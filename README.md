

<h1 align="center">Data Prep Kit</h1>

![alt text](doc/Data-prep-kit-diagram.png)

<div align="center"> 

<?  [![Status](https://img.shields.io/badge/status-active-success.svg)]() ?>
<?  [![GitHub Issues](https://img.shields.io/github/issues/kylelobo/The-Documentation-Compendium.svg)](https://github.com/IBM/data-prep-kit/issues) ?>
<?  [![GitHub Pull Requests](https://img.shields.io/github/issues-pr/kylelobo/The-Documentation-Compendium.svg)](https://github.com/IBM/data-prep-kit/pulls) ?>
</div> 

## &#x1F4D6; About <a name = "about"></a>

Data Prep Kit is a community-driven project simplifying unstructured data preparation for LLM application development. It addresses the growing challenge of preparing diverse data (language, code, vision, multimodal) for fine-tuning, instruction-tuning, and RAG applications. 

Features of the toolkit: 

- The kit provides growing set of pre-built [modules/transforms](transforms) with sample implementations across multiple runtimes, targeting laptop-scale to datacenter-scale processing.
- These modules have been tested while producing pre-training datasets for the [Granite open source LLM models](https://huggingface.co/ibm-granite).
- Data modalities supported _today_: Natural Language and Code.
- Plug and play [complete data processing recipes](examples) that can be used for real enterprise use cases like RAG, fine-tuning etc.
- [Data processing library](data-processing-lib/ray) to enable contribution of new custom modules. Check out [guidance](ADVANCED.md) for advanced users from adding your transform to scaling and automation.
- How to [contribute](CONTRIBUTING.md).
- It uses [Kubeflow Pipelines](https://www.kubeflow.org/docs/components/pipelines/v1/introduction/)-based [workflow automation](kfp/doc/simple_transform_pipeline.md).
- The modules are built on common frameworks for Python, Spark and Ray runtimes.
- [Repository Structure and Use](doc/repo.md).
- Access [Resources (papers, talks, presentations and tutorials)](resources.md).


## &#x1F680; Getting Started <a name = "gettingstarted"></a>

### Fastest way to experience Data Prep Kit

With no setup necessary, let's use a Google Colab friendly notebook to try Data Prep Kit. This is a simple transform to extract content from PDF files: [examples/notebooks/Run_your_first_transform_colab.ipynb](examples/notebooks/Run_your_first_transform_colab.ipynb)  | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/IBM/data-prep-kit/blob/dev/examples/notebooks/Run_your_first_transform_colab.ipynb). ([Here](doc/google-colab.md) are some tips for running Data Prep Kit transforms on Google Colab. For this simple example, these tips are either already taken care of, or are not needed.)  The same notebook can be downloaded and run on the local machine, without cloning the repo or any other setup. For additional guidance on setting up Jupyter lab, click [here](doc/quick-start/quick-start.md#jupyter). 

### Install data prep kit from PyPi

The latest version of the Data Prep Kit is available on PyPi for Python 3.10, 3.11 or 3.12. It can be installed using: 

```bash
pip install  'data-prep-toolkit-transforms[ray,all]'
```

The above installs all available transforms. 

When installing select transforms, users can specify the name of the transform in the pip command, rather than [all]. For example, use the following command to install only the pdf2parquet transform:
```bash
pip install 'data-prep-toolkit-transforms[pdf2parquet]'
```
For additional guidance on creating the virtual environment for installing the data prep kit, click [here](doc/quick-start/quick-start.md#conda).

### Run your first data prep pipeline

Now that you have run a single transform, the next step is to explore how to put these transforms 
together to run a data prep pipeline for an end to end use case like fine tuning a model or building 
a RAG application. 
This [notebook](examples/notebooks/fine%20tuning/code/sample-notebook.ipynb) gives an example of 
how to build an end to end data prep pipeline for fine tuning for code LLMs. 
You can also explore how to build a RAG pipeline [here](examples/notebooks/rag).

### Windows users

Please click [here](doc/quick-start/quick-start.md#running-transforms-on-windows) for guidance on how to run transforms in Windows. 

### Current list of transforms 
The matrix below shows the the combination of modules and supported runtimes. All the modules can be accessed [here](transforms) and can be combined to form data processing pipelines, as shown in the [examples](examples/notebooks) folder. 


| Modules                                                                              |    Python-only     |        Ray         |       Spark        |     KFP on Ray     |
|:-------------------------------------------------------------------------------------|:------------------:|:------------------:|:------------------:|:------------------:|
| **Data Ingestion**                                                                   |                    |                    |                    |                    |
| [Code (from zip) to Parquet](transforms/code/code2parquet/python/README.md) | :white_check_mark: | :white_check_mark: |                    | :white_check_mark: |
| [PDF to Parquet](transforms/language/pdf2parquet/README.md)                 | :white_check_mark: | :white_check_mark: |                    | :white_check_mark: |
| [HTML to Parquet](transforms/language/html2parquet/README.md)               | :white_check_mark: | :white_check_mark: |                    | :white_check_mark: |
| [Web to Parquet](transforms/universal/web2parquet/README.md)                | :white_check_mark: |                    |                    |                |         
| **Universal (Code & Language)**                                                      |                    |                    |                    |                    | 
| [Exact dedup filter](transforms/universal/ededup/README.md)                      | :white_check_mark: | :white_check_mark: |                    | :white_check_mark: |
| [Fuzzy dedup filter](transforms/universal/fdedup/README.md)                      | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| [Unique ID annotation](transforms/universal/doc_id/README.md)                    | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| [Filter on annotations](transforms/universal/filter/README.md)                   | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| [Profiler](transforms/universal/profiler/python/README.md)                       | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| [Resize](transforms/universal/resize/python/README.md)                           | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| [Hate, Abuse, Profanity (HAP)](transforms/universal/hap/README.md)               | :white_check_mark: | :white_check_mark: |                    | :white_check_mark: |
| [Tokenizer](transforms/universal/tokenization/README.md)                         | :white_check_mark: | :white_check_mark: |                    | :white_check_mark: |
| **Language-only**                                                                    |                    |                    |                    |                    |
| [Language identification](transforms/language/lang_id/README.md)              | :white_check_mark: | :white_check_mark: |                    | :white_check_mark: |
| [Document quality](transforms/language/doc_quality/README.md)                 | :white_check_mark: | :white_check_mark: |                    | :white_check_mark: |
| [Document chunking for RAG](transforms/language/doc_chunk/README.md)          | :white_check_mark: | :white_check_mark: |                    | :white_check_mark: |
| [Text encoder](transforms/language/text_encoder/README.md)                    | :white_check_mark: | :white_check_mark: |                    | :white_check_mark: |
| [PII Annotator/Redactor](transforms/language/pii_redactor/README.md)          | :white_check_mark: | :white_check_mark: |                    | :white_check_mark: |
| [Similarity](transforms/language/similarity/README.md)                        | :white_check_mark: |                    |                    |                    |
| **Code-only**                                                                         |                    |                     |             |                    |
| [Programming language annotation](transforms/code/proglang_select/python/README.md)  | :white_check_mark: | :white_check_mark: |                    | :white_check_mark: |
| [Code quality annotation](transforms/code/code_quality/python/README.md)             | :white_check_mark: | :white_check_mark: |                    | :white_check_mark: |
| [Malware annotation](transforms/code/malware/python/README.md)                       | :white_check_mark: | :white_check_mark: |                    | :white_check_mark: |
| [Header cleanser](transforms/code/header_cleanser/python/README.md)                  | :white_check_mark: | :white_check_mark: |                    | :white_check_mark: |
| [Semantic file ordering](transforms/code/repo_level_ordering/ray/README.md)          |                    | :white_check_mark: |                    |                    |
| [License Select Annotation](transforms/code/license_select/python/README.md)         | :white_check_mark: | :white_check_mark: |                    | :white_check_mark: |
| [Code profiler](transforms/code/code_profiler/README.md)                             | :white_check_mark: | :white_check_mark: |                    |  |


Contributors are welcome to add new modules to expand to other data modalities as well as add runtime support for existing modules!

## Citations <a name = "citations"></a>

If you use Data Prep Kit in your research, please cite our paper:

```bash
@misc{wood2024dataprepkitgettingdataready,
      title={Data-Prep-Kit: getting your data ready for LLM application development}, 
      author={David Wood and Boris Lublinsky and Alexy Roytman and Shivdeep Singh 
      and Constantin Adam and Abdulhamid Adebayo and Sungeun An and Yuan Chi Chang 
      and Xuan-Hong Dang and Nirmit Desai and Michele Dolfi and Hajar Emami-Gohari 
      and Revital Eres and Takuya Goto and Dhiraj Joshi and Yan Koyfman 
      and Mohammad Nassar and Hima Patel and Paramesvaran Selvam and Yousaf Shah  
      and Saptha Surendran and Daiki Tsuzuku and Petros Zerfos and Shahrokh Daijavad},
      year={2024},
      eprint={2409.18164},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2409.18164}, 
}
```
