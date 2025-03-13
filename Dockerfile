FROM python:3.11-slim

# We change to a directory unique to us
WORKDIR /airbyte/async_api

# Copy source files
COPY ./ . 

# Install Python dependencies
RUN python -m pip install ./

# When this container is invoked, append the input argemnts to `python source.py`
ENTRYPOINT ["python", "/airbyte/async_api/main.py"]

# Airbyte's build system uses these labels to know what to name and tag the docker images produced by this Dockerfile.
LABEL io.airbyte.name=airbyte/source-async-api
LABEL io.airbyte.version=0.1.0

# In order to launch a source on Kubernetes in a pod, we need to be able to wrap the entrypoint.
# The source connector must specify its entrypoint in the AIRBYTE_ENTRYPOINT variable.
ENV AIRBYTE_ENTRYPOINT='python /airbyte/async_api/main.py'
