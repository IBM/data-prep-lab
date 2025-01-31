# Bloom Annotation
Please see the set of [transform project conventions](../../README.md#transform-project-conventions) for details on general project conventions, transform configuration, testing and IDE set up.

## Contributor
- Yang Zhao (yangzhao@ibm.com)

## Description
### Prerequisite 
Please refer to `requirements.txt` to install the necessary packages.

### Overview
The bloom transform maps a non-empty input table to an output table with an added `is_in_GneissWeb` column. Each row in the table corresponds to a UUID and its associated document. The Bloom transform verifies whether the document's UUID exists in the GneissWeb Bloom filter.


### input format
The input is in .parquet format and contains the following columns:

| id  | contents | 
|:------:|:------:|
| &lt;urn:uuid:39147604-bfbe-4ed5-b19c-54105f8ae8a7&gt;  |   Viewing Single Post From: Spoilers for the We...   |
| &lt;urn:uuid:ba819eb7-e6e6-415a-87f4-0347b6a4f017&gt;  |    *sigh* Fundamentalist community, let me pass o...  |


### output format
The output is in .parquet format and includes an additional column, in addition to those in the input:

| id  | contents | is_in_GneissWeb  |
|:------:|:------:|:------:|
| &lt;urn:uuid:39147604-bfbe-4ed5-b19c-54105f8ae8a7&gt;  |    Viewing Single Post From: Spoilers for the We...   | 0     |
| &lt;urn:uuid:ba819eb7-e6e6-415a-87f4-0347b6a4f017&gt;  |    *sigh* Fundamentalist community, let me pass o...  | 1     |

## Configuration 
The set of dictionary keys holding [BLOOMTransformConfiguration](dpk_bloom/transform.py) 
configuration for values are as follows:


* --model_name_or_path - specify the GneissWeb Bloom filter model, which should be sourced from HuggingFace. The default is the test Bloom filter model.
* --batch_size - modify it based on the infrastructure capacity. Defaults to `1000`.
* --doc_text_column - the column name containing the document text in the input .parquet file. Defaults to `contents`.
* --annotation_column - the column name containing binary score in the output .parquet file. Defaults to `is_in_GneissWeb`.
  



## Usage
Place your input Parquet file in the `test-data/input/` directory. A sample file, `test1.parquet`, is available in this directory. Once done, run the script.

```python
python local_python.py
```

You will obtain the output file `test1.parquet` in the output directory.

### Code example
[notebook](bloom_python.ipynb)


## Testing

Currently we have:
- [bloom test](test/test_bloom.py)
