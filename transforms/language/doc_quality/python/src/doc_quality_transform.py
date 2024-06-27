# (C) Copyright IBM Corp. 2024.
# Licensed under the Apache License, Version 2.0 (the “License”);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#  http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an “AS IS” BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
################################################################################

from argparse import ArgumentParser, Namespace
from typing import Any

import os
import pyarrow as pa
from data_processing.data_access import DataAccessFactory, DataAccess
from data_processing.transform import AbstractTableTransform, TransformConfiguration
from data_processing.utils import CLIArgumentProvider, TransformUtils, get_logger
from doc_c4_statistics import (
    c4_contain_pattern_ratio,
    c4_contains_ldnoobw_words,
    c4_load_ldnoobw_words,
    c4_sentence_count,
)
from doc_Gopher_statistics import (
    compute_average_japanese_sentence_length,
    compute_bullet_point_ellipsis_alphabet_word_ratio,
    compute_word_statistics,
    contains_common_English_words,
    find_first_japanese_alphabet_position,
)
from perplexity import (
    get_model_file_name,
    get_tokenizer_file_name,
    KenLMModel,
    MODEL_FILE_NAME_SUFFIX,
    TOKENIZER_FILE_NAME_SUFFIX,
)

logger = get_logger(__name__)

short_name = "docq"
cli_prefix = f"{short_name}_"
text_lang_key = "text_lang"
doc_content_column_key = "doc_content_column"
doc_id_column_key = "doc_id_column"
bad_word_filepath_key = "bad_word_filepath"
kenLM_model_key = "kenLM_model"
text_lang_cli_param = f"{cli_prefix}{text_lang_key}"
doc_content_column_cli_param = f"{cli_prefix}{doc_content_column_key}"
doc_id_column_cli_param = f"{cli_prefix}{doc_id_column_key}"
bad_word_filepath_cli_param = f"{cli_prefix}{bad_word_filepath_key}"
kenLM_model_cli_param = f"{cli_prefix}{kenLM_model_key}"

data_factory_internal_key = f"{cli_prefix}data_factory"
files_to_use_internal_key = f"{cli_prefix}files_to_use"

class DocQualityTransform(AbstractTableTransform):
    """
    Implements a simple copy of a pyarrow Table.
    """

    def __init__(self, config: dict[str, Any]):
        """
        Initialize based on the dictionary of configuration information.
        This is generally called with configuration parsed from the CLI arguments defined
        by the companion runtime, DocQualityTransformRuntime.  If running inside the RayMutatingDriver,
        these will be provided by that class with help from the RayMutatingDriver.
        """
        # Make sure that the param name corresponds to the name used in apply_input_params method
        # of DocQualityTransformConfiguration class
        super().__init__(config)
        self.text_lang = config.get(text_lang_key)
        self.doc_content_column = config.get(doc_content_column_key)
        self.doc_id_column = config.get(doc_id_column_key)
        self.bad_word_filepath = config.get(bad_word_filepath_key)

        self.re_pattern = c4_load_ldnoobw_words(ft_lang=self.text_lang, file_path=self.bad_word_filepath)

        self.kenLM_model = config.get(kenLM_model_key, None)
        if self.kenLM_model is None:
            raise RuntimeError(f"Missing configuration value for key {kenLM_model_key}")
        daf = config.get(data_factory_internal_key, None)
        if os.path.exists(self.kenLM_model):
            logger.info(f"Load kenLM model found locally")
            self.klm = KenLMModel.from_pretrained(
                model_path=self.kenLM_model, language=self.text_lang, strip_accent=True
            )
        else:
            logger.info(f"Load kenLM model from remote")
            data_access = daf.create_data_access()
            import tempfile
            with tempfile.TemporaryDirectory() as temp_dir:
                # use a temporary directory until model is loaded to memory
                self._write_locally(data_access, self.kenLM_model, get_model_file_name(self.text_lang), temp_dir)
                self._write_locally(data_access, self.kenLM_model, get_tokenizer_file_name(self.text_lang), temp_dir)
                self.klm = KenLMModel.from_pretrained(
                    model_path=temp_dir, language=self.text_lang, strip_accent=True
                )

    def _write_locally(self, data_access: DataAccess, path: str, filename: str, temp_dir: str):
        content = data_access.get_file(os.path.join(path, filename))
        temp_file_path = os.path.join(temp_dir, filename)
        with open(temp_file_path, 'wb') as temp_file:
            temp_file.write(content)

    def transform(self, table: pa.Table, file_name: str = None) -> tuple[list[pa.Table], dict[str, Any]]:
        """
        Put Transform-specific to convert one Table to 0 or more tables. It also returns
        a dictionary of execution statistics - arbitrary dictionary
        """
        docq_total_words = []
        docq_mean_word_len = []
        docq_symbol_to_word_ratio = []
        docq_sentence_count = []
        docq_curly_bracket_ratio = []
        docq_lorem_ipsum_ratio = []
        docq_contain_bad_word = []
        docq_bullet_point_ratio = []
        docq_ellipsis_line_ratio = []
        docq_alphabet_word_ratio = []
        docq_contain_common_en_words = []
        docq_perplex_score = []
        if self.text_lang == "ja":
            # for japanese language, add 2 extra columns for 2 heuristic rules:
            docq_avg_ja_sentence_len = []
            docq_first_ja_alphabet_pos = []

        for text in table[self.doc_content_column].to_pylist():
            total_words, mean_word_len, symbol_to_word_ratio = compute_word_statistics(text)
            docq_total_words.append(total_words)
            docq_mean_word_len.append(mean_word_len)
            docq_symbol_to_word_ratio.append(symbol_to_word_ratio)

            docq_sentence_count.append(c4_sentence_count(text, ft_lang=self.text_lang))

            docq_lorem_ipsum_ratio.append(
                c4_contain_pattern_ratio(text, pattern="lorem ipsum", ft_lang=self.text_lang, normalize_text=True)
            )
            curly_bracket_ratio = 0.0
            for sign in ["{", "}"]:
                curly_bracket_ratio += c4_contain_pattern_ratio(
                    text, pattern=sign, ft_lang=self.text_lang, normalize_text=False
                )
            docq_curly_bracket_ratio.append(curly_bracket_ratio)
            docq_contain_bad_word.append(c4_contains_ldnoobw_words(text, self.re_pattern))

            (
                bullet_point_ratio,
                ellipsis_line_ratio,
                alphabet_word_ratio,
            ) = compute_bullet_point_ellipsis_alphabet_word_ratio(text)
            docq_bullet_point_ratio.append(bullet_point_ratio)
            docq_ellipsis_line_ratio.append(ellipsis_line_ratio)
            docq_alphabet_word_ratio.append(alphabet_word_ratio)

            docq_contain_common_en_words.append(contains_common_English_words(text, self.text_lang))

            docq_perplex_score.append(self.klm.get_perplexity(text))

            if self.text_lang == "ja":
                docq_avg_ja_sentence_len.append(compute_average_japanese_sentence_length(text))
                docq_first_ja_alphabet_pos.append(find_first_japanese_alphabet_position(text))

        table = TransformUtils.add_column(table=table, name="docq_total_words", content=docq_total_words)
        table = TransformUtils.add_column(table=table, name="docq_mean_word_len", content=docq_mean_word_len)
        table = TransformUtils.add_column(
            table=table, name="docq_symbol_to_word_ratio", content=docq_symbol_to_word_ratio
        )
        table = TransformUtils.add_column(table=table, name="docq_sentence_count", content=docq_sentence_count)
        table = TransformUtils.add_column(table=table, name="docq_lorem_ipsum_ratio", content=docq_lorem_ipsum_ratio)
        table = TransformUtils.add_column(
            table=table, name="docq_curly_bracket_ratio", content=docq_curly_bracket_ratio
        )
        table = TransformUtils.add_column(table=table, name="docq_contain_bad_word", content=docq_contain_bad_word)
        table = TransformUtils.add_column(table=table, name="docq_bullet_point_ratio", content=docq_bullet_point_ratio)
        table = TransformUtils.add_column(
            table=table, name="docq_ellipsis_line_ratio", content=docq_ellipsis_line_ratio
        )
        table = TransformUtils.add_column(
            table=table, name="docq_alphabet_word_ratio", content=docq_alphabet_word_ratio
        )
        table = TransformUtils.add_column(
            table=table, name="docq_contain_common_en_words", content=docq_contain_common_en_words
        )
        table = TransformUtils.add_column(table=table, name="metakenlm_docq_perplex_score", content=docq_perplex_score)

        if self.text_lang == "ja":
            table = table.append_column("docq_avg_ja_sentence_len", pa.array(docq_avg_ja_sentence_len))
            table = table.append_column("docq_first_ja_alphabet_pos", pa.array(docq_first_ja_alphabet_pos))

        metadata = {
            "total_docs_count": table.num_rows,
        }

        return [table], metadata


class DocQualityTransformConfiguration(TransformConfiguration):

    """
    Provides support for configuring and using the associated Transform class include
    configuration with CLI args.
    """
    def __init__(self):
        super().__init__(
            name=short_name,
            transform_class=DocQualityTransform,
            remove_from_metadata=[data_factory_internal_key],
        )
        self.daf = None

    def add_input_params(self, parser: ArgumentParser) -> None:
        """
        Add Transform-specific arguments to the given  parser.
        This will be included in a dictionary used to initialize the DocQualityTransform.
        By convention a common prefix should be used for all transform-specific CLI args
        (e.g, noop_, pii_, etc.)
        """
        parser.add_argument(
            f"--{text_lang_cli_param}",
            default="en",
            help="language used in the text content"
        )
        parser.add_argument(
            f"--{doc_content_column_cli_param}",
            default="contents",
            help="column name that contains document text",
        )
        parser.add_argument(
            f"--{doc_id_column_cli_param}",
            default="document_id",
            help="column name that contains document id",
        )
        parser.add_argument(
            f"--{bad_word_filepath_cli_param}",
            type=str,
            required=True,
            help="path to bad word file: local folder (file or directory) that points to bad word file",
        )
        parser.add_argument(
            f"--{kenLM_model_cli_param}",
            type=str,
            required=True,
            help="path to kenLM model: local folder (file or directory) that points to kenLM model",
        )
        self.daf = DataAccessFactory(cli_prefix, False)
        self.daf.add_input_params(parser)

    def apply_input_params(self, args: Namespace) -> bool:
        """
        Validate and apply the arguments that have been parsed
        :param args: user defined arguments.
        :return: True, if validate pass or False otherwise
        """
        captured = CLIArgumentProvider.capture_parameters(args, cli_prefix, False)
        self.params = self.params | captured | {
            data_factory_internal_key: self.daf,
        }
        logger.info(f"doc_quality parameters are : {self.params}")
        # Validate and populate the transform's DataAccessFactory
        return self.daf.apply_input_params(args)