# Code Profiler Transform 


## Configuration and command line Options

The set of dictionary keys holding [code_profiler_transform](src/code_profiler_transform.py) 
configuration for values are as follows:

* content - specifies the column name in the dataframe that has the code snippet
* language - specifies the programming languages of the code snippet

## Running

### Launched Command Line Options 
The following command line arguments are available in addition to 
the options provided by 
the [python launcher](../../../../data-processing-lib/doc/python-launcher-options.md).

### Running the samples

The code profiler can be run on mach-arm64 and x86_64 host architecture.
Depending on your host architecture, please change the `RUNTIME_HOST_ARCH` in the Makefile.
```
# values possible mach-arm64, x86_64
export RUNTIME_HOST_ARCH=x86_64
```
If you are using mac, you may need to permit your Mac to load the .so from the security settings. Generally, you get the pop-up under the tab security while running the transform.

![alt text](image.png)

To run the samples, use the following `make` targets

* `run-local-sample` - runs src/code_profiler_local.py
* `run-local-python-sample` - runs src/code_profiler_local_python.py

These targets will activate the virtual environment and set up any configuration needed.
Use the `-n` option of `make` to see the detail of what is done to run the sample.

For example, 
```shell
make run-local-sample
...
```
Then 
```shell
ls output
```
To see results of the transform.

### Transforming data using the transform image

To use the transform image to transform your data, please refer to the 
[running images quickstart](../../../../doc/quick-start/run-transform-image.md),
substituting the name of this transform image and runtime as appropriate.
