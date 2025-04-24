#!/bin/bash

# Build the Docker image
docker build -t ai-assistant -f docker/Dockerfile.assistant .

# Run the container interactively with AWS credentials mounted
docker run -it \
  --rm \
  -v ~/.aws:/root/.aws:ro \
  -e AWS_DEFAULT_PROFILE=default \
  ai-assistant
