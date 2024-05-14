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

# Collection of code data specific annotations and its heuristics are borrowed from:
# CodeParrot  https://github.com/huggingface/transformers/tree/main/examples/research_projects/codeparrot#preprocessing
# BigCode Dataset https://github.com/bigcode-project/bigcode-dataset/tree/main/preprocessing
#
# Code specific heuristics like alpha numeric, char token ratio implementations & others are taken from CodeParrot and BigCode Dataset
# preprocessing scripts and modified according to data-prep-kit specific framework.


import os
from argparse import ArgumentParser, Namespace

import numpy as np
import pyarrow as pa
from bs4 import BeautifulSoup
from data_processing.runtime.pure_python.transform_configuration import (
    PythonTransformRuntimeConfiguration,
)
from data_processing.runtime.ray import RayTransformLauncher
from data_processing.runtime.ray.transform_configuration import (
    RayTransformRuntimeConfiguration,
)
from data_processing.transform import AbstractTableTransform, TransformConfiguration
from data_processing.utils import TransformUtils
from transformers import AutoTokenizer


CODE_QUALITY_PARAMS = "code_quality_params"
os.environ["TOKENIZERS_PARALLELISM"] = "false"


def is_xml(data, lang):
    """
    Check if input data is xml content
    """
    if lang.lower() != "xslt" and "<?xml version=" in data[:100]:
        return True
    return False


def is_html(data, lang):
    """
    Check if input data is HTML files based on displayed text VS code ratio
    """
    if lang.lower() == "html":
        html = data
        try:
            soup = BeautifulSoup(html, features="html.parser")
        except:
            return True

        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()  # rip it out

        # get text
        text = soup.get_text()
        ratio = len(text) / len(html)
        if ratio > 0.2 and len(text) > 100:
            return True
    return False


# CODEPARROT FILTERS
def calculate_line_stats(data, lines_max=7):
    """
    Calculates mean and max line length of file
    """
    line_lengths = np.array([len(line) for line in data.splitlines()])
    if line_lengths.shape[0] < lines_max:
        lines_max = line_lengths.shape[0]
    longest_lines = np.sort(line_lengths)[::-1][:lines_max]
    return {
        "line_mean": np.mean(line_lengths),
        "line_max": np.max(line_lengths),
        "avg_longest_lines": np.mean(longest_lines),
        "num_lines": line_lengths.shape[0],
    }


def calculate_alpha_stats(data):
    """
    Calculates mean alpha numeric of input data
    """
    alphanum_frac = np.mean([c.isalnum() for c in data])
    return {"alphanum_frac": alphanum_frac}


def calculate_char_token_ratio(data, tokenizer):
    """
    Compute character/token ratio of the file with tokenizer.
    """
    input_ids = tokenizer(data, truncation=False)["input_ids"]
    ratio = len(data) / len(input_ids)
    return {"char_token_ratio": ratio}


def is_autogenerated(data, scan_width=5):
    """
    Check if file is autogenerated by looking for keywords in the first few lines of the file.
    """
    keywords = ["auto-generated", "autogenerated", "automatically generated"]
    lines = data.splitlines()
    for _, line in zip(range(scan_width), lines):
        for keyword in keywords:
            if keyword in line.lower():
                return True
    else:
        return False


def is_config_or_test(data, scan_width=5, coeff=0.2):
    """
    Check if file is a configuration file or a unit test by :
    1- looking for keywords in the first few lines of the file.
    2- counting number of occurrences of the words 'config' and 'test' with respect to number of lines.
    """
    keywords = ["unit tests", "test file", "configuration file"]
    lines = data.splitlines()
    count_config = 0
    count_test = 0
    # first test
    for _, line in zip(range(scan_width), lines):
        for keyword in keywords:
            if keyword in line.lower():
                return True
    # second test
    nlines = data.count("\n")
    threshold = int(coeff * nlines)
    for line in lines:
        count_config += line.lower().count("config")
        count_test += line.lower().count("test")
        if count_config > threshold or count_test > threshold:
            return True
    return False


def has_no_keywords(data, language):
    """
    Check if a python file has none of the keywords for: funcion, class, for loop, while loop.
    """
    if language.lower() == "python":
        keywords = ["def ", "class ", "for ", "while "]
        lines = data.splitlines()
        for line in lines:
            for keyword in keywords:
                if keyword in line.lower():
                    return False
        return True
    return False


def has_few_assignments(data, language, minimum=4):
    """
    Check if file uses symbol '=' less than `minimum` times.
    """
    langs_to_inspect = [
        "java",
        "python",
        "c",
        "c++",
        "c#",
        "go",
        "javascript",
        "go",
        "ruby",
        "perl",
        "swift",
        "rust",
        "r",
        "matlab",
    ]

    if language.lower() in langs_to_inspect:
        lines = data.splitlines()
        counter = 0
        for line in lines:
            counter += line.lower().count("=")
            if counter > minimum:
                return False
        return True
    return False


class CodeQualityTransform(AbstractTableTransform):
    """
    Defines Code Quality specific annotation for code data. Some of the methods inspired from CodeParrot and StarCoder.
    """

    def __init__(self, config: dict):
        super().__init__(config)

        self.code_quality = config.get(CODE_QUALITY_PARAMS)
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.code_quality["tokenizer"], use_auth_token=self.code_quality["hf_token"]
        )

    def transform(self, table: pa.Table) -> tuple[list[pa.Table], dict]:
        """
        Chain all preprocessing steps into one function to not fill cache.
        """

        if not TransformUtils.validate_columns(
            table, [self.code_quality["contents_column_name"], self.code_quality["language_column_name"]]
        ):
            return [], {}

        line_mean_values = []
        line_max_values = []
        no_lines_values = []
        avg_longest_lines_values = []
        alphanum_frac_values = []
        char_token_ratio_values = []
        is_autogenerated_values = []
        is_config_or_test_values = []
        has_no_keywords_values = []
        has_few_assignments_values = []
        is_xml_values = []
        is_html_values = []

        contents = table.column(self.code_quality["contents_column_name"]).to_pylist()
        languages = table.column(self.code_quality["language_column_name"]).to_pylist()

        # loop over rows and compute filter stats
        for i, c in enumerate(contents):
            # compute lines statistics
            stats = calculate_line_stats(c)
            line_mean_values.append(stats["line_mean"])
            line_max_values.append(stats["line_max"])
            no_lines_values.append(stats["num_lines"])
            avg_longest_lines_values.append(stats["avg_longest_lines"])

            alphanum_frac_values.append(calculate_alpha_stats(c)["alphanum_frac"])
            char_token_ratio_values.append(calculate_char_token_ratio(c, self.tokenizer)["char_token_ratio"])

            is_autogenerated_values.append(is_autogenerated(c))
            is_config_or_test_values.append(is_config_or_test(c))
            has_no_keywords_values.append(has_no_keywords(c, languages[i]))
            has_few_assignments_values.append(has_few_assignments(c, languages[i]))
            is_xml_values.append(is_xml(c, languages[i]))
            is_html_values.append(is_html(c, languages[i]))

        columns_exist = []
        for column_name in [
            "line_mean",
            "line_max",
            "total_num_lines",
            "avg_longest_lines",
            "alphanum_frac",
            "char_token_ratio",
            "autogenerated",
            "config_or_test",
            "has_no_keywords",
            "has_few_assignments",
            "is_xml",
            "is_html",
        ]:
            if column_name in table.schema.names:
                columns_exist.append(column_name)

        table = table.drop_columns(columns_exist)
        annotated_table = (
            table.append_column("line_mean", [line_mean_values])
            .append_column("line_max", [line_max_values])
            .append_column("total_num_lines", [no_lines_values])
            .append_column("avg_longest_lines", [avg_longest_lines_values])
            .append_column("alphanum_frac", [alphanum_frac_values])
            .append_column("char_token_ratio", [char_token_ratio_values])
            .append_column("autogenerated", [is_autogenerated_values])
            .append_column("config_or_test", [is_config_or_test_values])
            .append_column("has_no_keywords", [has_no_keywords_values])
            .append_column("has_few_assignments", [has_few_assignments_values])
            .append_column("is_xml", [is_xml_values])
            .append_column("is_html", [is_html_values])
        )

        return [annotated_table], {}


class CodeQualityTransformConfiguration(TransformConfiguration):
    def __init__(self):
        super().__init__(name="code_quality", transform_class=CodeQualityTransform)

    def add_input_params(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            "--cq_contents_column_name",
            required=False,
            type=str,
            dest="contents_column_name",
            default="contents",
            help="Name of the column holds the data to process",
        )
        parser.add_argument(
            "--cq_language_column_name",
            required=False,
            type=str,
            dest="language_column_name",
            default="language",
            help="Name of the column holds the programming language details.",
        )
        parser.add_argument(
            "--cq_tokenizer",
            required=False,
            type=str,
            dest="tokenizer",
            default="codeparrot/codeparrot",
            help="Name or path to the tokenizer.",
        )
        parser.add_argument(
            "--cq_hf_token",
            required=False,
            type=str,
            dest="hf_token",
            default=None,
            help="Huggingface auth token to download and use the tokenizer.",
        )

    def apply_input_params(self, args: Namespace) -> bool:
        dargs = vars(args)

        self.params = {
            CODE_QUALITY_PARAMS: {
                "contents_column_name": dargs.get("contents_column_name"),
                "language_column_name": dargs.get("language_column_name"),
                "tokenizer": dargs.get("tokenizer"),
                "hf_token": dargs.get("hf_token"),
            }
        }

        return True


class CodeQualityRayTransformConfiguration(RayTransformRuntimeConfiguration):
    def __init__(self):
        super().__init__(base_configuration=CodeQualityTransformConfiguration())


class CodeQualityPythonTransformConfiguration(PythonTransformRuntimeConfiguration):
    def __init__(self):
        super().__init__(base_configuration=CodeQualityTransformConfiguration())


if __name__ == "__main__":
    launcher = RayTransformLauncher(CodeQualityRayTransformConfiguration())
    launcher.launch()
