# Document ID Python Annotator

Please see the set of [transform project conventions](../../../README.md) for details on general project conventions,
transform configuration, testing and IDE set up.

## Contributors
- Boris Lublinsky (blublinsk@ibm.com)

## Description

This transform assigns unique identifiers to the documents in a dataset and supports the following annotations to the
original data:
* **Adding a Document Hash** to each document. The unique hash-based ID is generated using
`hashlib.sha256(doc.encode("utf-8")).hexdigest()`. To store this hash in the data specify the desired column name using
the `hash_column` parameter.
* **Adding an Integer Document ID**: to each document. The integer ID is unique across all rows and tables processed by
the `transform()` method. To store this ID in the data, specify the desired column name using the `int_id_column`
parameter.

Document IDs are essential for tracking annotations linked to specific documents. They are also required for processes
like [fuzzy deduplication](../../fdedup/README.md), which depend on the presence of integer IDs. If your dataset lacks document ID
columns, this transform can be used to generate them.

## Input Columns Used by This Transform

| Input Column Name                                                | Data Type | Description                      |
|------------------------------------------------------------------|-----------|----------------------------------|
| Column specified by the _contents_column_ configuration argument | str       | Column that stores document text |

## Output Columns Annotated by This Transform
| Output Column Name | Data Type | Description                                 |
|--------------------|-----------|---------------------------------------------|
| hash_column        | str       | Unique hash assigned to each document       |
| int_id_column      | uint64    | Unique integer ID assigned to each document |

## Configuration and Command Line Options

The set of dictionary keys defined in [DocIDTransform](src/doc_id_transform_base.py)
configuration for values are as follows:

* _doc_column_ - specifies name of the column containing the document (required for ID generation)
* _hash_column_ - specifies name of the column created to hold the string document id, if None, id is not generated
* _int_id_column_ - specifies name of the column created to hold the integer document id, if None, id is not generated
* _start_id_ - an id from which ID generator starts () 

At least one of _hash_column_ or _int_id_column_ must be specified.

## Usage

### Launched Command Line Options 
When running the transform with the Ray launcher (i.e. TransformLauncher),
the following command line arguments are available in addition to 
[the options provided by the ray launcher](../../../../data-processing-lib/doc/ray-launcher-options.md).
```
  --doc_id_doc_column DOC_ID_DOC_COLUMN
                        doc column name
  --doc_id_hash_column DOC_ID_HASH_COLUMN
                        Compute document hash and place in the given named column
  --doc_id_int_column DOC_ID_INT_COLUMN
                        Compute unique integer id and place in the given named column
  --doc_id_start_id DOC_ID_START_ID
                        starting integer id
```
These correspond to the configuration keys described above.

### Running the samples
To run the samples, use the following `make` targets

* `run-cli-sample` - runs src/doc_id_transform_python.py using command line args
* `run-local-sample` - runs src/doc_id_local_python.py

These targets will activate the virtual environment and set up any configuration needed.
Use the `-n` option of `make` to see the detail of what is done to run the sample.

For example, 
```shell
make run-cli-sample
...
```
Then 
```shell
ls output
```
To see results of the transform.

### Code example

[notebook](../doc_id.ipynb)

### Transforming data using the transform image

To use the transform image to transform your data, please refer to the 
[running images quickstart](../../../../doc/quick-start/run-transform-image.md),
substituting the name of this transform image and runtime as appropriate.

## Testing

Following [the testing strategy of data-processing-lib](../../../../data-processing-lib/doc/transform-testing.md)

Currently we have:
- [Unit test](test/test_doc_id_python.py)
- [Integration test](test/test_doc_id.py)
