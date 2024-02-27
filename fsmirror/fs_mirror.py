#!/usr/bin/env python

# standard library
import os
import sys
import json
import pathlib
import hashlib
import typing
import datetime

# third party
import yaml


class FSMirrorException(Exception): pass


def load_config(path:str = None) -> dict:
    if path:
        config = yaml.safe_load(pathlib.Path(path).read_text())
        return config
    else:
        CONFIG_PATH = os.getenv('FSMIRROR_CONFIG_PATH')
        try:
            config = yaml.safe_load(pathlib.Path(CONFIG_PATH).read_text())
            return config
        except Exception as e:
            raise FSMirrorException("Environment variable FSMIRROR_CONFIG_PATH must be set!")
    return None


class FSMirror:
    def __init__ (
            self,
            config: dict,
            mirror: str = 'orchestrator',
            id_method: str = 'date',
            take_last_instance: bool = True,
            ):
        """
        Parameters
        ----------
        config: dict of loaded config `yaml.safe_load(pathlib.Path(CONFIG_PATH).read_text()) -> dict`
        mirror: str of the root subdirectory to split on
        id_method: str of method to use for generating ids options: ['date', 'uuid']
        take_last_instance: bool of whether or not to take the final instance
        """
        self._config = config
        self._mirror = mirror
        if mirror not in config['mirrors']:
            raise FSMirrorException(f"Couldn't find mirror {mirror} please check the mirrors defined in your config")
        self._root = self._config['mirrors'][mirror]['root']
        self._prefix = self._config['mirrors'][mirror]['prefix']
        self._output_name = self._config['mirrors'][mirror]['output_name']
        self._output_format = self._config['mirrors'][mirror]['output_format']
        self._id = self._generate_id()
        self._take_last = take_last_instance
 

    def _generate_id (
            self,
            method: str = 'date',
            custom_func: typing.Optional[callable] = None,
            ) -> str:
        """
Generate ids
        
        Parameters
        ----------
        method: str of method to use for generating id: ['date', 'uuid']
        custom_func: callable custom function to generate ids with

        Returns
        ---------
        id: str
        """
        if method == 'date':
            return datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S')
        elif method == 'uuid':
            return str(uuid.uuid4())
        else:
            raise FSMirrorException(f"unknown id method {method}")


    def get_last_root_ix (
            self,
            path_parts: typing.List[str]
            ) -> int:
        """
Get the last index of the root for mirroring.
        """
        maxid = None
        for i in range(len(path_parts)):
            if path_parts[i] == self._root:
                maxid = i
        return maxid


    def mirror_relative (
            self,
            obj: typing.Any,
            with_id: bool = True,
            ) -> str:
        """
Mirror a class or function and return the relative path

        Parameters
        ----------
        obj: any object to mirror around
        with_id: bool of whether or not to generate a unique id

        Returns
        ---------
        path: str of relative path
        """
        if callable(obj):
            module = sys.modules[obj.__module__]
            name = obj.__name__
        elif hasattr(obj, '__class__'):
            module = sys.modules[obj.__class__.__module__]
            name = f"{obj.__module__}/{obj.__class__.__name__}"
        else:
            raise FSMirrorException(f"FSMirror can only mirror classes or functions")

        parts = module.__file__.split('/')
        if self._take_last:
            base_ix = self.get_last_root_ix(parts)
        else:
            base_ix = parts.index(self._root)
        if base_ix == -1:
            raise FSMirrorException(f"module {module.__file__} has no subdirectory: {self._root}")
        base = parts[base_ix:]
        # clean up .py, .pyc, etc.
        base = list(map(lambda x: x if '.' not in x else x.split('.')[0], base))
        base = "/".join(base)
        if with_id:
            return f"{base}/{name}/{self._id}"
        else:
            return f"{base}/{name}"


    def mirror_full (
            self,
            obj: typing.Any,
            with_id: bool = True
            ) -> str:
        """
Mirror a class or function and return the full path

        Parameters
        ----------
        obj: any object to mirror around
        with_id: bool of whether or not to generate a unique id

        Returns
        ---------
        path: str of relative path
        """

        relative = self.mirror_relative(obj, with_id=with_id)
        if self._config['storage']['provider'] == 'local':
            return f"{self._config['storage']['tenant']}/{relative}"
        elif self._config['storage']['provider'] in ['s3', 'gcs', 'blob', 'hdfs']:
            return f"{self._config['storage']['provider']}://{self._config['storage']['tenant']}/{relative}"
        return None


    def mirror_relative_output (
            self,
            obj: typing.Any,
            with_id: bool = True,
            ) -> str:
        """
Mirror a class or function and return the relative path

        Parameters
        ----------
        obj: any object to mirror around
        with_id: bool of whether or not to generate a unique id

        Returns
        ---------
        path: str of relative path
        """
        relative = self.mirror_relative(obj, with_id=with_id)
        return f"{relative}/{self._output_name}.{self._output_format}"


    def mirror_full_output (
            self,
            obj: typing.Any,
            with_id: bool = True
            ) -> str:
        """
Mirror a class or function and return the full path

        Parameters
        ----------
        obj: any object to mirror around
        with_id: bool of whether or not to generate a unique id

        Returns
        ---------
        path: str of full path
        """

        fullpath = self.mirror_full(obj, with_id=with_id)
        return f"{fullpath}/{self._output_name}.{self._output_format}"
