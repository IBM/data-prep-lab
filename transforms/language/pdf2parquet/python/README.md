# Ingest PDF to Parquet Transform

Please see the set of
[transform project conventions](../../../README.md#transform-project-conventions)
for details on general project conventions, transform configuration,
testing and IDE set up.

## Contributors

- Michele Dolfi (dol@zurich.ibm.com)

## Description 

This tranforms iterate through document files or zip of files and generates parquet files
containing the converted document in Markdown or JSON format.

The PDF conversion is using the [Docling package](https://github.com/DS4SD/docling).
The Docling configuration in DPK is tuned for best results when running large batch ingestions.
For more details on the multiple configuration options, please refer to the official [Docling documentation](https://ds4sd.github.io/docling/).


### Input files

This transform supports the following input formats:

- PDF documents
- DOCX documents
- PPTX presentations
- Image files (png, jpeg, etc)
- HTML pages
- Markdown documents
- ASCII Docs documents

The input documents can be provided in a folder structure, or as a zip archive.
Please see the configuration section for specifying the input files.


### Output format

The output table will contain following columns

| output column name | data type | description |
|-|-|-|
| source_filename | string | the basename of the source archive or file |
| filename | string | the basename of the PDF file |
| contents | string | the content of the PDF |
| document_id | string | the document id, a random uuid4  |
| document_hash | string | the document hash of the input content |
| ext | string | the detected file extension |
| hash | string | the hash of the `contents` column |
| size | string | the size of `contents` |
| date_acquired | date | the date when the transform was executing |
| num_pages | number | number of pages in the PDF |
| num_tables | number | number of tables in the PDF |
| num_doc_elements | number | number of document elements in the PDF |
| pdf_convert_time | float | time taken to convert the document in seconds |



## Configuration

The transform can be initialized with the following parameters.

| Parameter  | Default  | Description  |
|------------|----------|--------------|
| `data_files_to_use`          | - | The files extensions to be considered when running the transform. Example value `['.pdf','.docx','.pptx','.zip']`. For all the supported input formats, see the section above. |
| `batch_size`                 | -1 | Number of documents to be saved in the same result table. A value of -1 will generate one result file for each input file. |
| `artifacts_path`             | <unset> | Path where to Docling models artifacts are located, if unset they will be downloaded and fetched from the [HF_HUB_CACHE](https://huggingface.co/docs/huggingface_hub/en/guides/manage-cache) folder. |
| `contents_type`         | `text/markdown`        | The output type for the `contents` column. Valid types are `text/markdown`, `text/plain` and `application/json`. |
| `do_table_structure`         | `True`        | If true, detected tables will be processed with the table structure model. |
| `do_ocr`                     | `True`        | If true, optical character recognition (OCR) will be used to read the content of bitmap parts of the document. |
| `ocr_engine`                 | `easyocr`     | The OCR engine to use. Valid values are `easyocr`, `tesseract`, `tesseract_cli`. |
| `bitmap_area_threshold`      | `0.05`        | Threshold for running OCR on bitmap figures embedded in document. The threshold is computed as the fraction of the area covered by the bitmap, compared to the whole page area. |
| `pdf_backend`                | `dlparse_v2`  | The PDF backend to use. Valid values are `dlparse_v2`, `dlparse_v1`, `pypdfium2`. |
| `double_precision`           | `8`           | If set, all floating points (e.g. bounding boxes) are rounded to this precision. For tests it is advised to use 0. |


Example

```py
{
    "data_files_to_use": ast.literal_eval("['.pdf','.docx','.pptx','.zip']"),
    "contents_type": "application/json",
    "do_ocr": True,
}
```

## Usage

### Launched Command Line Options 

When invoking the CLI, the parameters must be set as `--pdf2parquet_<name>`, e.g. `--pdf2parquet_do_ocr=true`.


### Running the samples
To run the samples, use the following `make` targets

* `run-cli-sample` - runs src/pdf2parquet_transform_python.py using command line args
* `run-local-sample` - runs src/pdf2parquet_local.py
* `run-local-python-sample` - runs src/pdf2parquet_local_python.py

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

See the sample script [src/pdf2parquet_local_python.py](src/pdf2parquet_local_python.py).


### Transforming data using the transform image

To use the transform image to transform your data, please refer to the 
[running images quickstart](../../../../doc/quick-start/run-transform-image.md),
substituting the name of this transform image and runtime as appropriate.

## Testing

Following [the testing strategy of data-processing-lib](../../../../data-processing-lib/doc/transform-testing.md)

Currently we have:
- [Unit test](transforms/language/pdf2parquet/python/test/test_pdf2parquet_python.py)
- [Integration test](transforms/language/pdf2parquet/python/test/test_pdf2parquet.py)


## Credits

The PDF document conversion is developed by the AI for Knowledge group in IBM Research Zurich.
The main package is [Docling](https://github.com/DS4SD/docling).
