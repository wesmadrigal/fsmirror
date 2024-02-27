#!/usr/bin/env python

# standard lib
import os

# third party
import pytest

# internal
from fsmirror import FSMirror, load_config


class SomeTask(object):
    def __init__(self):
        pass

    def run(self):
        print('running')


def some_task(x):
    print(x)


config_path = '/'.join(os.path.abspath(__file__).split('/')[0:-2])+'/examples/config.yml'
config = load_config(config_path)


def test_instantiation_with_mirror(): 
    fm = FSMirror(config=config, mirror='fsmirror')
    assert True


def test_mirror_full():
    # relative path
    fm = FSMirror(config=config, mirror='fsmirror')
    full = f"s3://test.bucket/fsmirror/tests/test_mirror/SomeTask/{fm._id}"
    output = fm.mirror_full(SomeTask)
    assert full == output


def test_mirror_relative():
    fm = FSMirror(config=config, mirror='fsmirror') 
    output = fm.mirror_relative(SomeTask)
    assert output == f'fsmirror/tests/test_mirror/SomeTask/{fm._id}'


def test_mirror_relative_output():
    fm = FSMirror(config=config, mirror='fsmirror')
    print(fm.mirror_relative_output(some_task))
    output = fm.mirror_relative_output(some_task)
    assert output == f'fsmirror/tests/test_mirror/some_task/{fm._id}/out.parquet'


def test_mirror_relative_output_no_id():
    fm = FSMirror(config=config, mirror='fsmirror')
    print(fm.mirror_relative_output(some_task, with_id=False))
    output = fm.mirror_relative_output(some_task, with_id=False)
    assert output == f'fsmirror/tests/test_mirror/some_task/out.parquet'


def test_mirror_full_output():
    fm = FSMirror(config=config, mirror='fsmirror')
    print(fm.mirror_full_output(some_task))
    output = fm.mirror_full_output(some_task)
    assert output == f's3://test.bucket/fsmirror/tests/test_mirror/some_task/{fm._id}/out.parquet'


def test_mirror_full_output_no_id():
    fm = FSMirror(config=config, mirror='fsmirror')
    print(fm.mirror_full_output(some_task, with_id=False))
    output = fm.mirror_full_output(some_task, with_id=False)
    assert output == f's3://test.bucket/fsmirror/tests/test_mirror/some_task/out.parquet'


if __name__ == '__main__':  
    from fsmirror import load_config, FSMirror

    config_path = '/'.join(os.path.abspath(__file__).split('/')[0:-2])+'/examples/config.yml'
    config = load_config(config_path)

    mirror = FSMirror(config=config, mirror='fsmirror')


    print(mirror.mirror_full(SomeTask))
    print(mirror.mirror_relative(SomeTask))

    print(mirror.mirror_full(some_task))
    print(mirror.mirror_relative(some_task))

    print(mirror.mirror_full(some_task, with_id=False))
    print(mirror.mirror_relative(some_task, with_id=False))

    print("")
