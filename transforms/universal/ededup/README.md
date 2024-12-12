# Exact Deduplication Transform 

Exact deduplication transform identifies and removes identical documents in a dataset by comparing them hash-for-hash
to ensure exact matching. Per the set of [transform project conventions](../../README.md#transform-project-conventions)
the following runtimes are available:

* [python](python/README.md) - enables running of the base python transformation in a Python runtime
* [ray](ray/README.md) - enables running of the base python transformation in a Ray runtime
* [kfp](kfp_ray/README.md) - enables running the ray docker image in a kubernetes cluster using a generated `yaml` file.

Please see [here](python/README.md) a more detailed description of this transform.
