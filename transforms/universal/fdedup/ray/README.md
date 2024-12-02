# Fuzzy Dedup

Please see the set of [transform project conventions](../../../README.md) for details on general project conventions, transform
configuration,  testing and IDE set up.

## Summary

This project wraps the [Fuzzy Dedup transform](../python) with a Ray runtime.

## Configuration and command line Options

Fuzzy Dedup configuration and command line options are the same as for the base python transform. 

## Running
### Launched Command Line Options 
When running the transform with the Ray launcher (i.e. TransformLauncher),
In addition to those available to the transform as defined in [here](../python/README.md),
the set of 
[ray launcher](../../../../data-processing-lib/doc/ray-launcher-options.md) are available.

### Running the samples
To run the samples, use the following `make` target to create a virtual environment:

```commandline
make venv
```
Subsequently, the main orchestration program can run with:
```commandline
source venv/bin/activate
cd src
python fdedup_transform_ray.py
```
Alternatively the transforms included in fuzzy dedup can be launched independently:
```commandline
source venv/bin/activate
cd src
python signature_calc_local_ray.py
python cluster_analysis_local_ray.py
python get_duplicate_list_local_ray.py
python data_cleaning_local_ray.py
```
After running the transforms, execute:
```shell
ls output
```
To see results of the transform.

### Transforming data using the transform image

To use the transform image to transform your data, please refer to the 
[running images quickstart](../../../../doc/quick-start/run-transform-image.md),
substituting the name of this transform image and runtime as appropriate.

## Testing

For testing fuzzy deduplication in a ray runtime, use the following `make` targets. To launch integration tests
for all the component transforms of fuzzy dedup (signature calculation, cluster analysis, get duplicate list and data
cleaning) use: 
```commandline
make test-src
```

To test the creation of the Docker image for fuzzy dedup transform and the capability to run a local program inside that
image, use:
```commandline
make test-image
```