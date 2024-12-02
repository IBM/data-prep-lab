# Ingest PDF to Parquet Ray Transform 
Please see the set of
[transform project conventions](../../../README.md#transform-project-conventions)
for details on general project conventions, transform configuration,
testing and IDE set up.

This module implements the ray version of the [pdf2parquet transform](../python/).

## Summary 
This project wraps the [Ingest PDF to Parquet transform](../python) with a Ray runtime.

## Configuration and command line Options

Ingest PDF to Parquet configuration and command line options are the same as for the base python transform. 

## Running

### Launched Command Line Options 
When running the transform with the Ray launcher (i.e. TransformLauncher),
In addition to those available to the transform as defined in [here](../python/README.md),
the set of 
[ray launcher](../../../../data-processing-lib/doc/ray-launcher-options.md) are available.

### Running the samples
To run the samples, use the following `make` targets

* `run-cli-sample` - runs src/pdf2parquet_transform_ray.py using command line args
* `run-local-sample` - runs src/pdf2parquet_local_ray.py
* `run-s3-sample` - runs src/pdf2parquet_s3_ray.py
    * Requires prior invocation of `make minio-start` to load data into local minio for S3 access.

These targets will activate the virtual environment and set up any configuration needed.
Use the `-n` option of `make` to see the detail of what is done to run the sample.

For example, 
```shell
make run-cli-sample
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


## Prometheus metrics

The transform will produce the following statsd metrics:

| metric name                      | Description                                                      |
|----------------------------------|------------------------------------------------------------------|
| worker_pdf_doc_count             | Number of PDF documents converted by the worker                  |
| worker_pdf_pages_count           | Number of PDF pages converted by the worker                      |
| worker_pdf_page_avg_convert_time | Average time for converting a single PDF page on each worker     |
| worker_pdf_convert_time          | Time spent converting a single document                          |

