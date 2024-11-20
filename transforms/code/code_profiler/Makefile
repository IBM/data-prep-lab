REPOROOT=../../..
# Use make help, to see the available rules
include $(REPOROOT)/.make.defaults

setup::
	@# Help: Recursively make $@ all subdirs 
	$(MAKE) RULE=$@ .recurse

clean::
	@# Help: Recursively make $@ all subdirs 
	$(MAKE) RULE=$@ .recurse

build::
	@# Help: Recursively make $@ in subdirs 
	$(MAKE) RULE=$@ .recurse
venv::
	@# Help: Recursively make $@ in subdirs 
	$(MAKE) RULE=$@ .recurse

publish:: 
	@# Help: Recursively make $@ in all subdirs 
	@$(MAKE) RULE=$@ .recurse

test-image:
	@echo "Skipping test-image step as per configuration."

test:: 
	@# Help: Recursively make $@ in all subdirs 
	@$(MAKE) RULE=$@ .recurse

test-src::
	@# Help: Recursively make $@ in all subdirs 
	$(MAKE) RULE=$@ .recurse

set-versions:
	@# Help: Recursively $@ in all subdirs
	$(MAKE) RULE=$@ .recurse

.PHONY: workflow-venv
workflow-venv:

.PHONY: workflow-test
workflow-test:

.PHONY: workflow-upload
workflow-upload:

.PHONY: workflow-build
workflow-build:
