#!/usr/bin/env bash

# Update package lists
apt-get update 

# Install system dependencies for lxml
apt-get install -y \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    python3-dev \
    build-essential \
    pkg-config

# Upgrade pip to the latest version
pip3 install --upgrade pip setuptools wheel

# Install lxml using a precompiled wheel to avoid compilation issues
pip3 install --no-build-isolation --no-cache-dir --prefer-binary lxml

pip3 install unstructured[all] unstructured-client

# Install the rest of your dependencies
pip3 install -r requirements.txt
