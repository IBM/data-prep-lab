# Fuzzy Deduplication Transform 
The fdedup transform eliminates documents that are highly similar to each other (but not necessarily identical) from a
set of Parquet files. This ensures that the resulting dataset contains only unique or sufficiently distinct entries.
Per the set of [transform project conventions](../../README.md#transform-project-conventions) the following runtimes are available:

* [python](python/README.md) - enables running the base transform in a pure python environment
* [ray](ray/README.md) - enables running the base python transform in a Ray runtime
* [spark](spark/README.md) - enables running the base python transform in a spark runtime
* [kfp](kfp_ray/README.md) - enables running the ray docker image in a kubernetes cluster using a generated `yaml` file.

Please check [here](python/README.md) for a more detailed description of this transform.
