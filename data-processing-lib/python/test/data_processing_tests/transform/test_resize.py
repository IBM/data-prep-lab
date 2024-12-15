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

from data_processing.test_support.transform import ResizePythonTransformConfiguration
from data_processing.runtime.pure_python import PythonTransformLauncher
from data_processing.test_support.launch.transform_test import (
    AbstractTransformLauncherTest,
)


class TestPythonResizeTransform(AbstractTransformLauncherTest):
    """
    Extends the super-class to define the test data for the tests defined there.
    The name of this class MUST begin with the word Test so that pytest recognizes it as a test class.
    """

    def get_test_transform_fixtures(self) -> list[tuple]:
        # The following based on 3 identical input files of about 39kbytes, and 200 rows
        fixtures = []
        basedir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                               "../../../../../transforms/universal/resize/python/test-data"))
        launcher = PythonTransformLauncher(ResizePythonTransformConfiguration())

        # Split into 4 or so files
        config = {"resize_max_rows_per_table": 125}
        fixtures.append((launcher, config, basedir + "/input", basedir + "/expected-rows-125"))

        # Merge into 2 or so files
        config = {"resize_max_rows_per_table": 300}
        fixtures.append((launcher, config, basedir + "/input", basedir + "/expected-rows-300"))

        # # Merge all into a single table
        config = {"resize_max_mbytes_per_table": 1}
        fixtures.append((launcher, config, basedir + "/input", basedir + "/expected-mbytes-1"))

        # # Merge the 1st 2 and some of the 2nd with the 3rd
        config = {"resize_max_mbytes_per_table": 0.05}
        fixtures.append((launcher, config, basedir + "/input", basedir + "/expected-mbytes-0.05"))

        # Split into 4 or so files
        config = {"resize_max_mbytes_per_table": 0.02}
        fixtures.append((launcher, config, basedir + "/input", basedir + "/expected-mbytes-0.02"))

        return fixtures
