FROM mcr.microsoft.com/devcontainers/base:ubuntu-22.04

# Avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Core tools + Python (no ensurepip on Ubuntu system Python)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        sudo \
        vim \
        make \
        git \
        zip \
        tree \
        curl \
        wget \
        jq \
        software-properties-common \
        python3.11 \
        python3-pip \
        python3.11-venv \
        python3.11-dev && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1 && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Updated packaging toolchain
RUN python3 -m pip install --no-cache-dir --upgrade pip setuptools wheel

# Installing K3D for local Kubernetes development
RUN curl -s https://raw.githubusercontent.com/k3d-io/k3d/main/install.sh | bash

# Installing Tekton CLI (latest)
RUN set -eux; \
    ARCH="$(dpkg --print-architecture)"; \
    case "$ARCH" in \
      amd64) TKN_ARCH="Linux_x86_64" ;; \
      arm64) TKN_ARCH="Linux_arm64" ;; \
      *) echo "Unsupported architecture: $ARCH"; exit 1 ;; \
    esac; \
    TKN_VERSION="$(curl -fsSL https://api.github.com/repos/tektoncd/cli/releases/latest | jq -r .tag_name | sed 's/^v//')"; \
    curl -fsSLO "https://github.com/tektoncd/cli/releases/download/v${TKN_VERSION}/tkn_${TKN_VERSION}_${TKN_ARCH}.tar.gz"; \
    tar -xzf "tkn_${TKN_VERSION}_${TKN_ARCH}.tar.gz" -C /usr/local/bin tkn; \
    chmod +x /usr/local/bin/tkn; \
    rm -f "tkn_${TKN_VERSION}_${TKN_ARCH}.tar.gz"

# Install OpenShift CLI (stable latest)
RUN set -eux; \
    ARCH="$(dpkg --print-architecture)"; \
    case "$ARCH" in \
      amd64) OC_ARCH="linuxx86_64" ;; \
      arm64) OC_ARCH="linuxarm64" ;; \
      *) echo "Unsupported architecture: $ARCH"; exit 1 ;; \
    esac; \
    curl -fsSLO "https://mirror.openshift.com/pub/openshift-v4/clients/ocp/stable/${OC_ARCH}/openshift-client-${OC_ARCH}.tar.gz"; \
    tar -xzf "openshift-client-${OC_ARCH}.tar.gz" -C /usr/local/bin oc kubectl; \
    chmod +x /usr/local/bin/oc /usr/local/bin/kubectl; \
    rm -f "openshift-client-${OC_ARCH}.tar.gz"

WORKDIR /workspaces/${localWorkspaceFolderBasename}

ENV PORT=8000
EXPOSE 8000

# Enable color terminal for docker exec bash
ENV TERM=xterm-256color

# Do not set USER here; let devcontainer.json control remoteUser
