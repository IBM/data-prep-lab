# Ingest PDF to Parquet

This tranforms iterate through document files or zip of files and generates parquet files
containing the converted document in Markdown or JSON format.

The PDF conversion is using the [Docling package](https://github.com/DS4SD/docling).
The Docling configuration in DPK is tuned for best results when running large batch ingestions.
For more details on the multiple configuration options, please refer to the official [Docling documentation](https://ds4sd.github.io/docling/).

This transform supports the following input formats:

- PDF documents
- DOCX documents
- PPTX presentations
- Image files (png, jpeg, etc)
- HTML pages
- Markdown documents
- ASCII Docs documents


## Output format

The output format will contain all the columns of the metadata CSV file,
with the addition of the following columns

```jsonc
{
    "source_filename": "string",  // the basename of the source archive or file
    "filename": "string",         // the basename of the PDF file
    "contents": "string",         // the content of the PDF
    "document_id": "string",      // the document id, a random uuid4 
    "document_hash": "string",    // the document hash of the input content 
    "ext": "string",              // the detected file extension
    "hash": "string",             // the hash of the `contents` column
    "size": "string",             // the size of `contents`
    "date_acquired": "date",      // the date when the transform was executing
    "num_pages": "number",        // number of pages in the PDF
    "num_tables": "number",       // number of tables in the PDF
    "num_doc_elements": "number", // number of document elements in the PDF
    "pdf_convert_time": "float",  // time taken to convert the document in seconds
}
```


## Parameters

The transform can be initialized with the following parameters.

| Parameter  | Default  | Description  |
|------------|----------|--------------|
| `batch_size`                 | -1 | Number of documents to be saved in the same result table. A value of -1 will generate one result file for each input file. |
| `artifacts_path`             | <unset> | Path where to Docling models artifacts are located, if unset they will be downloaded and fetched from the [HF_HUB_CACHE](https://huggingface.co/docs/huggingface_hub/en/guides/manage-cache) folder. |
| `contents_type`         | `text/markdown`        | The output type for the `contents` column. Valid types are `text/markdown`, `text/plain` and `application/json`. |
| `do_table_structure`         | `True`        | If true, detected tables will be processed with the table structure model. |
| `do_ocr`                     | `True`        | If true, optical character recognition (OCR) will be used to read the content of bitmap parts of the document. |
| `ocr_engine`                 | `easyocr`     | The OCR engine to use. Valid values are `easyocr`, `tesseract`, `tesseract_cli`. |
| `bitmap_area_threshold`      | `0.05`        | Threshold for running OCR on bitmap figures embedded in document. The threshold is computed as the fraction of the area covered by the bitmap, compared to the whole page area. |
| `pdf_backend`                | `dlparse_v2`  | The PDF backend to use. Valid values are `dlparse_v2`, `dlparse_v1`, `pypdfium2`. |
| `double_precision`           | `8`           | If set, all floating points (e.g. bounding boxes) are rounded to this precision. For tests it is advised to use 0. |

When invoking the CLI, the parameters must be set as `--pdf2parquet_<name>`, e.g. `--pdf2parquet_do_ocr=true`.


## Credits

The PDF document conversion is developed by the AI for Knowledge group in IBM Research Zurich.
The main package is [Docling](https://github.com/DS4SD/docling).
