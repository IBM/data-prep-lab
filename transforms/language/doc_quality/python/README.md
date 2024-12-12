# Document Quality Transform 

Please see the set of
[transform project conventions](../../../README.md#transform-project-conventions)
for details on general project conventions, transform configuration,
testing and IDE set up.

## Contributors

- Daiki Tsuzuku (dtsuzuku@jp.ibm.com)

## Description 
This transform will calculate and annotate several metrics which are useful to assess the quality of the document.
The document quality transform operates on text documents only

### Input 

| input column name | data type | description |
|-|-|-|
| the one specified in _doc_content_column_ configuration | string | text whose quality will be calculated by this transform |

### Output columns annotated by this transform

| output column name | data type | description | supported language |
|-|-|-|-|
| docq_total_words | int | the total number of words | ALL |
| docq_mean_word_len | int | the mean of words' lengths | ALL |
| docq_symbol_to_word_ratio | float | the ratio of symbol-to-word ratio (Reference for symbols like emojis: https://textacy.readthedocs.io/en/0.11.0/api_reference/preprocessing.html, currently used symbol: `#`, `...`) | ALL |
| docq_sentence_count | int | the number of sentences | ALL |
| docq_curly_bracket_ratio | float | the ratio between the number of occurrences of `{` or `}` over the text length | ALL |
| docq_lorem_ipsum_ratio | float | the ratio between the number of occurrences of `lorem ipsum` over the text length. Lorem ipsum, or lipsum as it is sometimes known, is dummy text used in laying out print, graphic or web designs. | ALL |
| docq_contain_bad_word | bool | whether text containst bad words | ALL |
| docq_bullet_point_ratio | float | the ratio of lines starting with a bullet point | ALL |
| docq_ellipsis_line_ratio | float | the ratio of lines ending with an ellipsis | ALL |
| docq_alphabet_word_ratio | float | the ratio of words having at least one alphabetic character | ALL |
| docq_contain_common_en_words | bool | whether the given `text` contains common English words like `the`, `and`, `to`, `that`, `of`, `with`, `be`, and `have`| ALL |
| docq_avg_ja_sentence_len | int | average sentence length for an input text, inspired by an OSS HojiChar. | ja |
| docq_first_ja_alphabet_pos | int | first position of occurrence of Japanese alphabets (i.e., Hiragana or Katakana) | ja |

You can see more detailed backgrounds of some columns in [Deepmind's Gopher paper](https://arxiv.org/pdf/2112.11446.pdf)

## Configuration

The set of dictionary keys holding [DocQualityTransform](src/doc_quality_transform.py) 
configuration for values are as follows:

* _text_lang_ - specifies language used in the text content. By default, "en" is used.
* _doc_content_column_ - specifies column name that contains document text. By default, "contents" is used.
* _bad_word_filepath_ - specifies a path to bad word file: local folder (file or directory) that points to bad word file. You don't have to set this parameter if you don't need to set bad words.

Example
```
{
    text_lang_key: "en",
    doc_content_column_key: "contents",
    bad_word_filepath_key: os.path.join(basedir, "ldnoobw", "en"),
}
```

## Usage

### Launched Command Line Options 
The following command line arguments are available
```
  --docq_text_lang DOCQ_TEXT_LANG   language used in the text content. By default, "en" is used.
  --docq_doc_content_column DOCQ_DOC_CONTENT_COLUMN   column name that contain document text. By default, "contents" is used.
  --docq_bad_word_filepath DOCQ_BAD_WORD_FILEPATH   path to bad word file: local folder (file or directory) that points to bad word file. You don't have to set this parameter if you don't need to set bad words.
```
These correspond to the configuration keys described above.

### Running the samples
To run the samples, use the following `make` targets

* `run-cli-sample` - runs src/doc_quality_transform.py using command line args
* `run-local-sample` - runs src/doc_quality_local.py

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

[notebook](../doc_quality.ipynb)

### Transforming data using the transform image

To use the transform image to transform your data, please refer to the 
[running images quickstart](../../../../doc/quick-start/run-transform-image.md),
substituting the name of this transform image and runtime as appropriate.

## Testing

Following [the testing strategy of data-processing-lib](../../../../data-processing-lib/doc/transform-testing.md)

Currently we have:
- [Unit test](test/test_doc_quality_python.py)
- [Integration test](test/test_doc_quality.py)


## Further Resource

- For those who want to learn C4 heuristic rules
  - https://arxiv.org/pdf/1910.10683.pdf
- For those who want to learn Gopher statistics
  - https://arxiv.org/pdf/2112.11446.pdf
- For those who want to see the source of badwords used by default
  - https://github.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words


## Consideration

### Troubleshooting guide

For M1 Mac user, if you see following error during make command, `error: command '/usr/bin/clang' failed with exit code 1`, you may better follow [this step](https://freeman.vc/notes/installing-fasttext-on-an-m1-mac)