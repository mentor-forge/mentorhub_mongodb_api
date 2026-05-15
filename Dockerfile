# Use Configurator API Base Image
FROM ghcr.io/agile-learning-institute/mongodb_configurator_api:latest
LABEL org.opencontainers.image.source="{{org.git_host}}/{{org.git_org}}/{{info.slug}}_mongodb_api"

# Switch to root to set up /input directory
USER root

# Remove playground from base image
RUN rm -rf /input 

# Copy Configurations to the input folder (using absolute paths to preserve base image WORKDIR)
COPY configurator/api_deploy /input/api_config
COPY configurator/configurations /input/configurations
COPY configurator/dictionaries /input/dictionaries
COPY configurator/enumerators /input/enumerators
COPY configurator/migrations /input/migrations
COPY configurator/test_data /input/test_data
COPY configurator/types /input/types

# Create build timestamp
RUN echo $(date +'%Y%m%d-%H%M%S') > /input/api_config/BUILT_AT

# Set ownership to app user and make /input read-only
# Directories need execute permission (555) to be traversed
# Files can be read-only (444)
RUN chown -R app:app /input && \
    find /input -type d -exec chmod 555 {} \; && \
    find /input -type f -exec chmod 444 {} \;

# Switch back to app user (matching base image)
USER app

# Port Number for the API
ENV API_PORT={{info.base_port + 2}}
EXPOSE {{info.base_port + 2}}