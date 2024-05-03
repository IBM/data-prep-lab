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

import os

from data_processing.test_support.ray import AbstractTransformLauncherTest
from doc_id_transform import (
    DocIDTransform,
    DocIDTransformConfigurationRay,
    doc_column_name_cli_param,
    doc_column_name_key,
    hash_column_name_cli_param,
    hash_column_name_key,
    int_column_name_cli_param,
    int_column_name_key,
)


class TestRayDocIDTransform(AbstractTransformLauncherTest):
    """
    Extends the super-class to define the test data for the tests defined there.
    The name of this class MUST begin with the word Test so that pytest recognizes it as a test class.
    """

    def get_test_transform_fixtures(self) -> list[tuple]:
        basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../test-data"))
        fixtures = []
        config = {
            doc_column_name_cli_param: "contents",
            hash_column_name_cli_param: "doc_hash",
            int_column_name_cli_param: "doc_int",
        }
        fixtures.append((DocIDTransformConfigurationRay(), config, basedir + "/input", basedir + "/expected"))
        return fixtures
