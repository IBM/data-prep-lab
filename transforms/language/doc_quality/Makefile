REPOROOT=../../..
# Use make help, to see the available rules
include $(REPOROOT)/transforms/.make.cicd.targets

#
# This is intended to be included across the Makefiles provided within
# a given transform's directory tree,  so must use compatible syntax.
#
################################################################################
# This defines the name of the transform and is used to match against
# expected files and is used to define the transform's image name. 
TRANSFORM_NAME=$(shell basename `pwd`)

################################################################################



run-cli-sample:
	$(MAKE) RUN_FILE="-m dpk_$(TRANSFORM_NAME).transform_python" \
                RUN_ARGS=" --data_local_config \"{ 'input_folder' : '../test-data/input', 'output_folder' : '../output'}\"  \
                --docq_text_lang \"en\"	\
				--docq_doc_content_column \"contents\"	\
				--docq_bad_word_filepath \"../ldnoobw/en\" \
                .transforms.run-src-file


run-ray-cli-sample: 
	$(MAKE) RUN_FILE"-m dpk_$(TRANSFORM_NAME).ray.transform" \
                RUN_ARGS=" --run_locally True --data_local_config \"{ 'input_folder' : '../test-data/input', 'output_folder' : '../output'}\"  \
                --docq_text_lang \"en\"	\
				--docq_doc_content_column \"contents\"	\
				--docq_bad_word_filepath \"../ldnoobw/en\" \
                .transforms.run-src-file

