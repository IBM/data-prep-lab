# Similarity Transform 
Please see the set of
[transform project conventions](../../../README.md#transform-project-conventions)
for details on general project conventions, transform configuration, 
testing and IDE set up.

## Contributors
- Chad DeLuca (delucac@us.ibm.com)
- Anna Lisa Gentile (annalisa.gentile@ibm.com)

## Summary 
The similarity transforms annotates each input document with potential matches found in a document collection.
The annotation consists of a json object proving the id of the matched document in the collection and 
the specific sentenced deemed as "similar" by the tranform.
The Similarity Transorm relies on a running [ElasticSearch](https://www.elastic.co/elasticsearch) Index.

### Input files

This transform supports the input of [parquet files](https://parquet.apache.org/) that contain a single column, called "contents",
where each row is a a string that will be searched for in a target document collection.
The document collection is specified with configuration parameters.


### Output format

The output table will contain a single additional column:

| output column name | data type | description |
|-|-|-|
| contents | string | the original input text |
| similarity_score | json | the annotations that describe in which document a potential match was found and which sentence in the document was the closest match  |

Example of single cell contents in the output column:
```
I bet the company staffs want an increase in the wages
```

Example of single cell content in the similarity_score column:

```py
  {
      'contents': array(['I bet the company staffs want to have an increase in the wages.'], dtype=object), 
      'id': '123456789', 
      'index': 'myPrivateDocumentsIndex', 
      'score': 29.345
  }
```

## Configuration

The transform can be initialized with the following parameters.

| Parameter  | Default  | Description  |
|------------|----------|--------------|
| `similarity_es_endpoint` | - | The URL for Elasticsearch |
| `similarity_es_userid` | - | Elasticsearch user ID |
| `similarity_es_pwd` | - | Elasticsearch password |
| `similarity_es_index` | - | The Elasticsearch index to query |
| `similarity_shingle_size` | 8 | Shingle size for query construction (default is 8) |
| `similarity_result_size` | 1 | result size for matched sentences (default is 1) |
| `similarity_annotation_column` | similarity_score | The column name that will contain the similarity annotations, in json format |

Example

```py
{
      "similarity_es_pwd" :"my password",
      "similarity_es_userid":"myElasticsearchID",
      "similarity_es_endpoint":"https://thisIsWhere.MyElasticIsRunning.com",
      "similarity_es_index" :"myPrivateDocumentsIndex"
}
```

## Running

### Launched Command Line Options 
The following command line arguments are available in addition to 
the options provided by 
the [python launcher](../../../../data-processing-lib/doc/python-launcher-options.md).
```
  --similarity_es_endpoint SIMILARITY_ES_ENDPOINT
                        The URL for Elasticsearch
  --similarity_es_userid SIMILARITY_ES_USERID
                        Elasticsearch user ID
  --similarity_es_pwd SIMILARITY_ES_PWD
                        Elasticsearch password
  --similarity_es_index SIMILARITY_ES_INDEX
                        The Elasticsearch index to query
  --similarity_shingle_size SIMILARITY_SHINGLE_SIZE
                        Shingle size for query construction (default is 8)
  --similarity_result_size SIMILARITY_RESULT_SIZE
                        result size for matched sentences (default is 1)
  --similarity_annotation_column SIMILARITY_ANNOTATION_COLUMN
                        The column name that will contain the similarity score
  --similarity_doc_text_column SIMILARITY_DOC_TEXT_COLUMN
                        The column name that contains the document text
```
These correspond to the configuration keys described above.


### Launched Command Line Options 

When invoking the CLI, the parameters must be set as `--similarity_<name>`, e.g. `--similarity_es_pwd=pass`.

### Running the samples
To run the samples, use the following `make` targets

* `run-cli-sample` - runs python -m dpk_similarity.transform_python using command line args
* `run-local-sample` - runs python -m dpk_similarity.local
* `run-local-python-sample` - runs python -m dpk_similarity.local_python

These targets will activate the virtual environment and set up any configuration needed.
Use the `-n` option of `make` to see the detail of what is done to run the sample.

For example, 
```shell
make run-local-python-sample
...
```
Then 
```shell
ls output
```
To see results of the transform.

### Code example

TBD (link to the notebook will be provided)

