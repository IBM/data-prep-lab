# DPK Python Transforms

## installation

The [transforms](https://github.com/IBM/data-prep-kit/blob/dev/transforms/README.md) are delivered as a standard pyton library available on pypi and can be installed using pip install:

`python -m pip install data-prep-toolkit-transforms`
or
`python -m pip install data-prep-toolkit-transforms[ray]`


installing the python transforms will also install  `data-prep-toolkit`

installing the ray transforms will also install  `data-prep-toolkit[ray]`

## List of Transforms in current package

Note: This list includes the transforms that were part of the release starting with data-prep-toolkit-transforms:0.2.1. This list may not always reflect up to date information. Users are encourage to raise an issue in git when they discover missing components or packages that are listed below but not in the current release they get from pypi.

* code
    * [code2parquet](https://github.com/IBM/data-prep-kit/blob/dev/transforms/code/code2parquet/python/README.md)
    * [header_cleanser (Not available on MacOS)](https://github.com/IBM/data-prep-kit/blob/dev/transforms/code/header_cleanser/python/README.md)
    * [code_quality](https://github.com/IBM/data-prep-kit/blob/dev/transforms/code/code_quality/python/README.md)
    * [proglang_select](https://github.com/IBM/data-prep-kit/blob/dev/transforms/code/proglang_select/python/README.md)
* language
    * [doc_chunk](https://github.com/IBM/data-prep-kit/blob/dev/transforms/language/doc_chunk/python/README.md)
	* [doc_quality](https://github.com/IBM/data-prep-kit/blob/dev/transforms/language/doc_quality/python/README.md)
	* [lang_id](https://github.com/IBM/data-prep-kit/blob/dev/transforms/language/lang_id/python/README.md)
	* [pdf2parquet](https://github.com/IBM/data-prep-kit/blob/dev/transforms/language/pdf2parquet/python/README.md)
	* [text_encoder](https://github.com/IBM/data-prep-kit/blob/dev/transforms/language/text_encoder/python/README.md)
	* [pii_redactor](https://github.com/IBM/data-prep-kit/blob/dev/transforms/language/pii_redactor/python/README.md)
* universal
    * [ededup](https://github.com/IBM/data-prep-kit/blob/dev/transforms/universal/ededup/python/README.md)
	* [filter](https://github.com/IBM/data-prep-kit/blob/dev/transforms/universal/filter/python/README.md)
	* [resize](https://github.com/IBM/data-prep-kit/blob/dev/transforms/universal/resize/python/README.md)
	* [tokenization](https://github.com/IBM/data-prep-kit/blob/dev/transforms/universal/tokenization/python/README.md)
	* [doc_id](https://github.com/IBM/data-prep-kit/blob/dev/transforms/universal/doc_id/python/README.md)
	* [web2parquet](https://github.com/IBM/data-prep-kit/blob/dev/transforms/universal/web2parquet/README.md)
   
## Release notes:

### 0.2.3.dev1 
* code_profiler
### 0.2.3.dev0 
* fdedup
### 0.2.2.dev3 
* web2parquet
### 0.2.2.dev2
* pdf2parquet now supports HTML,DOCX,PPTX, ... in addition to PDF




 
