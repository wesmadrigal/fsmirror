# fsmirror

## Installation
```python
pip install fsmirror
```

### Functionality
Mirror project filesystems for metadata tracking.  It can be useful to have 
a direct path mirror between code that generates data and the location in a filesystem
or object store that stores the data / artifacts it generates.

### Usage

* Create a configuration file like the one in `examples/example_config.yml`
* Set the config path:
```bash
export FSMIRROR_CONFIG_PATH=/your/project/path/config.yml`
```

Use `fsmirror` for managing where to store artifacts, the following pseudocode is
an example of how it should be used:

```python
from some_data_pipeline import task
from storage_client import Client

from fsmirror.fsmirror import FSMirror, config

fm = FSMirror(config=config)

data = task()
storage_path = fm.mirror_relative(task, with_id=True)
Client.save_to_s3(storage_path)
```


