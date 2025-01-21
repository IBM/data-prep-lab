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


from data_processing.data_access import DataAccessHF

hf_conf = {
    "hf_token": None,
    "input_folder": 'datasets/blublinsky/test/data',
    "output_folder": 'datasets/blublinsky/test/temp/',
}


def test_hf_data_access():
    """
    Testing data access of HF data access
    :return: None
    """
    data_access = DataAccessHF(hf_config=hf_conf)
    # get files to process
    files, profile, retries = data_access.get_files_to_process()
    assert len(files) == 50
    assert profile['max_file_size'] >= 135.730997085571
    assert profile['min_file_size'] >= 0.00743961334228515
    assert profile['total_file_size'] >= 269.3791465759277

    random = data_access.get_random_file_set(n_samples=5, files=files)
    assert len(random) == 5

def test_hf_data_access_sets():
    """
    Testing data access of HF data access with data sets
    :return: None
    """
    data_access = DataAccessHF(hf_config=hf_conf, d_sets=["aai_Latn", "aba_Latn"])
    # get files to process
    files, profile, retries = data_access.get_files_to_process()
    assert len(files) == 4
    assert profile['max_file_size'] >= 0.501188278198242
    assert profile['min_file_size'] >= 0.00965785980224609
    assert profile['total_file_size'] >= 0.620627403259277
