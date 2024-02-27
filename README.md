# fsmirror

## Installation
```python
pip install fsmirror
```

### Functionality
Mirror project filesystems for metadata tracking.  It can be useful to have 
a direct path mirror between code that generates data and the location in a filesystem
or object store that stores the data / artifacts it generates.

### Example
code lives at: <br>
`project/etl/my_etl_task.py::LiftDataTask`
`fsmirror` output for associated: <br>
`project/etl/my_etl_task/LiftDataTask/out.parquet`
`fsmirror` s3 output for associated: <br>
`s3://my.bucket/project/etl/my_etl_task/LiftDataTask.out.parquet`


### Usage

* Create a configuration file like the one in `examples/example_config.yml`
* Set the config path:
```bash
export FSMIRROR_CONFIG_PATH=/your/project/path/config.yml`
```

The config file should look like the example:
```yaml
# artifacts
storage:
  # local, s3, gcs, blob
  provider: s3
  # root file path, bucket, etc.
  tenant: test.bucket
  # prefix - if 'MIRROR' will mirror filesystem
  namespace: MIRROR


# Each mirror should be a subdirectory
# within your project for example your
# orchestrator codebase lives at the
# following path:
#
# /opt/orchestrator
#
# To mirror this subdirectory we would
# add an "orchestrator" mirror as is
# done below
mirrors:
  fsmirror:
    # directory or subdirectory to split on
    root: fsmirror
    prefix: MIRROR
    output_name: out
    output_format: parquet

  aipipeline:
    root: aipipeline
    prefix: MIRROR
    output_name: out
    output_format: pkl
```

Use `fsmirror` for managing where to store artifacts, the following pseudocode is
an example of how it should be used:

```python
>>> from test_mirror import SomeTask, some_task
>>> from fsmirror import FSMirror, load_config
>>> load_config()
{'storage': {'provider': 's3', 'tenant': 'test.bucket', 'namespace': 'MIRROR'}, 'mirrors': {'fsmirror': {'root': 'fsmirror', 'prefix': 'MIRROR', 'output_name': 'out', 'output_format': 'parquet'}, 'aipipeline': {'root': 'aipipeline', 'prefix': 'MIRROR', 'output_name': 'out', 'output_format': 'pkl'}}}
>>> config = load_config()
>>> fm = FSMirror(config=config, mirror='fsmirror')
>>> fm.mirror_relative(some_task)
'fsmirror/tests/test_mirror/20240227160221/some_task'
>>> fm.mirror_relative(some_task, with_id=False)
'fsmirror/tests/test_mirror/some_task'
>>> fm.mirror_full(some_task)
's3://test.bucket/fsmirror/tests/test_mirror/20240227160221/some_task'
>>> fm.mirror_full_output(some_task)
's3://test.bucket/fsmirror/tests/test_mirror/20240227160221/some_task/out.parquet'
```


