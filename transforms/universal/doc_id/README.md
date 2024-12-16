# Doc ID Transform 

The Document ID transform assigns to each document in a dataset a unique identifier, including an integer ID and a
content hash, which can later be used by the exact dedup and fuzzy dedup transform to identify and remove duplicate
documents. Per the set of [transform project conventions](../../README.md#transform-project-conventions), the following
runtimes are available:

* [python](python/README.md) - enables running the base python transform in a Python runtime
* [ray](ray/README.md) - enables running the base python transform  in a Ray runtime
* [spark](spark/README.md) - enables running of a spark-based transform in a Spark runtime. 
* [kfp](kfp_ray/README.md) - enables running the ray docker image in a kubernetes cluster using a generated `yaml` file.

Please check [here](python/README.md) for a more detailed description of this transform.
