# Fuzzy Deduplication Ray-based KubeFlow Pipeline Transformation 


## Summary 
This project allows execution of the [fuzzy dedup Ray transform](../ray) as a 
[KubeFlow Pipeline](https://www.kubeflow.org/docs/components/pipelines/overview/)

The detail pipeline is presented in the [Simplest Transform pipeline tutorial](../../../../kfp/doc/simple_transform_pipeline.md) 

## Compilation

In order to compile pipeline definitions run
```shell
make workflow-build
```
from the directory. It creates a virtual environment (make workflow-venv) and after that compiles the pipeline 
definitions in the folder. The virtual environment is created once for all transformers. 

## Considerations
Currently, fuzzy dedup KFP pipeline definitions can be compiled and executed on KFPv1. KFPv2 is not
supported currently, because of this issue: https://github.com/kubeflow/pipelines/issues/10914

The next steps are described in [Deploying a pipeline](../../../../kfp/doc/simple_transform_pipeline.md#deploying-a-pipeline-)
and [Executing pipeline and watching execution results](../../../../kfp/doc/simple_transform_pipeline.md#executing-pipeline-and-watching-execution-results-)