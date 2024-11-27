# Pipelined transform

Typical DPK usage is a sequential invocation of individual transforms that process all of the input data and create 
the output one. Such execution is very convenient as it produces all of the intermediate data, which can be useful,
especially during the debugging. 

This said, such approach creates a lot of intermediate data and executes a lot of reads and writes, which might 
significantly slow down processing, especially in the case of large data sets.

To overcome this drawback, DPK introduced a new type of transform - pipeline transform. Pipeline transform 
(somewhat similar to [sklearn pipeline](https://scikit-learn.org/1.5/modules/generated/sklearn.pipeline.Pipeline.html)) 
is a transform, meaning it transforms one file at a time and a pipeline, meaning that this file is transformed by 
a set of individual transformers, passing data between then as a byte array in memory.

## Creating pipeline transform.

Creation of the pipeline transform requires creation of runtime specific transform runtime configuration 
leveraging [PipelineTransformConfiguration](../python/src/data_processing/transform/pipeline_transform_configuration.py)
Examples of such configuration can be found:

* [Python](../../transforms/universal/noop/python/src/noop_pipeline_transform_python.py)
* [Ray](../../transforms/universal/noop/ray/src/noop_pipeline_transform_ray.py)
* [Spark](../../transforms/universal/noop/spark/src/noop_pipeline_transform_spark.py)

These are very simple examples using pipeline containing a single transform.

More complex example defining pipeline of two examples - Resize and NOOP can be found
[Python](../python/src/data_processing/test_support/transform/pipeline_transform.py) and
[Ray](../ray/src/data_processing_ray/test_support/transform/pipeline_transform.py)

***Note*** the limitation of pipeline transform is that all participating transforms have to be different,
The same transform can not be included twice.

## Running pipeline transform

Similar to the `ordinary` transforms, pipeline transforms can be invoked using launcher, but parameters,
in this case have to include parameters for all participating transforms. The base class 
[AbstractPipelineTransform](../python/src/data_processing/transform/pipeline_transform.py) will initialize
all participating transforms based on these parameters

***Note*** as per DPK convention, parameters for every transform are prefixed by a transform name, which means
that a given transform will always get an appropriate parameter