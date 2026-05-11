FROM docker.io/debian:13-slim

ARG TARGETARCH
ENV DEBIAN_FRONTEND=noninteractive

# Install Curl, Tar, and Zip.
RUN apt-get update --ignore-missing && apt-get install --quiet --yes \
  build-essential curl git tar zip

# Install Just.
RUN curl -LSfs https://scruffaluff.github.io/picoware/install/just.sh | sh \
  -s -- --global

# Create non-priviledged user and grant user passwordless sudo.
RUN useradd --create-home --no-log-init debian \
    && usermod --append --groups sudo debian \
    && printf "debian ALL=(ALL) NOPASSWD:ALL\n" >> /etc/sudoers

ENV HOME=/home/debian USER=debian UV_LINK_MODE=copy
USER debian

# Disable Git dubious ownership warnings.
RUN git config --global --add safe.directory '*'
