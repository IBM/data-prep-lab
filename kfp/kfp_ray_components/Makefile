# Define the root of the local git clone for the common rules to be able
# # know where they are running from.
REPOROOT=../..

# Include the common rules.
# Use "make help" to see them.
include $(REPOROOT)/.make.defaults

#DOCKER_IMG=${DOCKER_HOSTNAME}/${DOCKER_NAMESPACE}/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_VERSION}
DOCKER_IMG=$(DOCKER_LOCAL_IMAGE)
BASE_IMAGE=${RAY_BASE_IMAGE}

ifeq ($(KFPv2), 1)
        DOCKER_IMAGE_NAME=kfp-data-processing_v2
else
        DOCKER_IMAGE_NAME=kfp-data-processing
endif

## removed from .make.defaults and set here before loading in kind
DOCKER_REMOTE_IMAGE=$(DOCKER_REGISTRY_ENDPOINT)/$(DOCKER_IMAGE_NAME):$(DOCKER_IMAGE_VERSION)

.PHONY: .lib-src-image
.lib-src-image:: .default.build-lib-wheel
	@$(eval LIB_WHEEL_FILE := $(shell find data-processing-dist/*.whl))
	$(eval LIB_WHEEL_FILE := $(shell basename $(LIB_WHEEL_FILE)))
	$(MAKE) .defaults.copy-lib LIB_PATH=$(REPOROOT)/kfp/kfp_support_lib/shared_workflow_support LIB_NAME=shared_workflow_support_lib
	$(MAKE) .defaults.copy-lib LIB_PATH=$(REPOROOT)/kfp/kfp_support_lib/$(WORKFLOW_SUPPORT_LIB) LIB_NAME=workflow_support_lib
	$(MAKE) DPK_WHEEL_FILE_NAME=$(LIB_WHEEL_FILE) .defaults.image
	rm -rf data-processing-dist
	rm -rf shared_workflow_support_lib
	rm -rf workflow_support_lib



.PHONY: build
build: image

.PHONY: image
image: Dockerfile requirements.txt
	$(MAKE) .lib-src-image


.PHONY: .reconcile-requirements
.reconcile-requirements:
	@sed -i.back "s/kfp-data-processing.*/$(DOCKER_IMAGE_NAME):${DOCKER_IMAGE_VERSION}\"/" ${FILE}

.PHONE: set-versions
set-versions:
	@# Help: Update yaml files to build images tagged as version $(DOCKER_IMAGE_VERSION).
	@$(MAKE) .reconcile-requirements FILE=createRayClusterComponent.yaml
	@$(MAKE) .reconcile-requirements FILE=deleteRayClusterComponent.yaml
	@$(MAKE) .reconcile-requirements FILE=executeRayJobComponent.yaml
	@$(MAKE) .reconcile-requirements FILE=executeRayJobComponent_multi_s3.yaml
ifneq ($(KFPv2), 1)
	@$(MAKE) .reconcile-requirements FILE=executeSubWorkflowComponent.yaml
endif

.PHONY: kind-load-image
kind-load-image:
	@# Help: Load the image to the kind cluster created with make setup.
	kind load docker-image $(DOCKER_REMOTE_IMAGE) --name=$(KIND_CLUSTER_NAME)

.PHONY: docker-load-image
docker-load-image:
	@$(MAKE) .defaults.docker-load-image

.PHONY: docker-save-image
docker-save-image:
	@$(MAKE) .defaults.docker-save-image

.PHONY: publish
publish:
	echo "Publishing kfp-data-processing"
	$(MAKE) KFPv2=0 DOCKER_IMAGE_NAME="kfp-data-processing" .defaults.publish-image
	echo "Publishing kfp-data-processing_v2"
	$(MAKE) KFPv2=1 DOCKER_IMAGE_NAME="kfp-data-processing_v2" .defaults.publish-image

test::

.PHONY: clean
clean:
	@# Help: Remove $(IMG)
	-rm  makeenv
	rm -rf *.back || true
