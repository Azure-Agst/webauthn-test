# Canvas2 Dockerfile
# By: Andrew Augustine

FROM python:3
LABEL org.opencontainers.image.authors="me@azureagst.dev"
LABEL org.opencontainers.image.source="https://github.com/Azure-Agst/webauthn-test"

# Set our image's working directory
# =============================================================================
# Essentially, this sets PWD for the following commands
WORKDIR /usr/src/app

# Copy in the requirements file first, then install them.
# =============================================================================
# This is done seperately from the rest of the files for a reason! Docker's 
# Getting Started tutorial explains this well, specifically the "Image Building
# Best Practices" section.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy in the rest of our app to the image
# =============================================================================
COPY . .

# Expose ports
# =============================================================================
EXPOSE 5000/tcp

# Set static env vars
# =============================================================================
ENV DOCKER_ENV=True
ENV FLASK_APP=webauthn-test
ENV FLASK_ENV=production

# Set the command to run the actual project
# =============================================================================
# - Entrypoint is the default command, non-negotiable
# - CMD are args appended that can be overridden at runtime
ENTRYPOINT [ "flask", "run" ]
CMD [ "--host", "0.0.0.0" ]