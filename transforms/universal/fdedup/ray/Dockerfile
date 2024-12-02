ARG BASE_IMAGE=docker.io/rayproject/ray:2.36.1-py310
FROM ${BASE_IMAGE}

RUN pip install --upgrade --no-cache-dir pip 

# install pytest
RUN pip install --no-cache-dir pytest
ARG DPK_WHEEL_FILE_NAME

# Copy and install data processing libraries 
# These are expected to be placed in the docker context before this is run (see the make image).
COPY --chown=ray:users data-processing-dist data-processing-dist
RUN  pip install data-processing-dist/${DPK_WHEEL_FILE_NAME}[ray]

## Copy the python version of the tansform
COPY --chown=ray:users python-transform/  python-transform/
RUN cd python-transform && pip install --no-cache-dir -e .

# Install ray project source
COPY --chown=ray:users src/ src/
COPY --chown=ray:users pyproject.toml pyproject.toml
COPY --chown=ray:users README.md README.md
COPY --chown=ray:users requirements.txt requirements.txt
RUN pip install --no-cache-dir -e .

# copy source files needed by test-image
COPY --chown=ray:users ./src/fdedup_transform_ray.py fdedup_transform_ray.py
COPY --chown=ray:users ./src/signature_calc_transform_ray.py signature_calc_transform_ray.py
COPY --chown=ray:users ./src/cluster_analysis_transform_ray.py cluster_analysis_transform_ray.py
COPY --chown=ray:users ./src/get_duplicate_list_transform_ray.py get_duplicate_list_transform_ray.py
COPY --chown=ray:users ./src/data_cleaning_transform_ray.py data_cleaning_transform_ray.py
COPY --chown=ray:users ./src/signature_calc_local_ray.py local/fdedup_local_ray.py

# copy test
COPY test/ test/
COPY test-data/ test-data/

USER root
RUN chmod a+rwx /home/ray
USER ray
# Set environment
ENV PYTHONPATH /home/ray

# Put these at the end since they seem to upset the docker cache.
ARG BUILD_DATE
ARG GIT_COMMIT
LABEL build-date=$BUILD_DATE
LABEL git-commit=$GIT_COMMIT
