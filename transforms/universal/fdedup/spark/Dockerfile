ARG BASE_IMAGE=data-prep-kit-spark-3.5.2:0.3.0
FROM ${BASE_IMAGE}

# install pytest
RUN pip install --no-cache-dir pytest
ARG DPK_WHEEL_FILE_NAME

WORKDIR ${SPARK_HOME}/work-dir

# Copy in the data processing framework source/project and install it
# This is expected to be placed in the docker context before this is run (see the make image).
COPY --chown=spark:root data-processing-dist data-processing-dist
RUN pip install data-processing-dist/${DPK_WHEEL_FILE_NAME}[spark]

## Copy the python version of the tansform
COPY --chown=spark:root python-transform/  python-transform/
RUN cd python-transform && pip install --no-cache-dir -e .

# Install spark project source
COPY --chown=spark:root src/ src/
COPY --chown=spark:root pyproject.toml pyproject.toml
COPY --chown=spark:root README.md README.md
RUN mkdir -p /opt/spark/work-dir/src/templates && \
    mkdir -p /opt/spark/work-dir/config
COPY --chown=spark:root deployment/kubernetes/spark-executor-pod-template.yml /opt/spark/work-dir/src/templates/
COPY --chown=spark:root deployment/kubernetes/spark_profile.yml /opt/spark/work-dir/config/

# install requirements from requirements.txt
COPY requirements.txt .
RUN pip3 install -r requirements.txt

RUN pip install --no-cache-dir -e .

# copy the main() entry point to the image
COPY ./src/fdedup_transform_spark.py .

# copy test
COPY test/ test/
COPY test-data/ test-data/

USER spark

# Set environment
ENV PYTHONPATH=${SPARK_HOME}/work-dir/:${SPARK_HOME}/work-dir/src/:${PYTHONPATH}
ENV PATH=${SPARK_HOME}/work-dir/.local/bin/:${PATH}

# Put these at the end since they seem to upset the docker cache.
ARG BUILD_DATE
ARG GIT_COMMIT
LABEL build-date=$BUILD_DATE
LABEL git-commit=$GIT_COMMIT
