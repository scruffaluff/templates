FROM docker.io/debian:13-slim

ARG TARGETARCH
ENV DEBIAN_FRONTEND=noninteractive

# Install essential packages.
RUN apt-get update --ignore-missing && apt-get install --quiet --yes \
  build-essential curl git sudo tar zip

# Install C compiler for Rust template.
RUN apt-get install --quiet --yes gcc

# Install C++ compiler for C++ template.
RUN apt-get install --quiet --yes g++

# Install Playwright dependencies for Vue template based on
# https://github.com/microsoft/playwright/blob/main/packages/playwright-core/src/server/registry/nativeDeps.ts#L1251.
RUN apt-get install --quiet --yes libasound2t64 libatk-bridge2.0-0t64 \
  libatk1.0-0t64 libatspi2.0-0t64 libcairo2 libcups2t64 libdbus-1-3 libdrm2 \
  libgbm1 libglib2.0-0t64 libnspr4 libnss3 libpango-1.0-0 libx11-6 libxcb1 \
  libxcomposite1 libxdamage1 libxext6 libxfixes3 libxkbcommon0 libxrandr2

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
