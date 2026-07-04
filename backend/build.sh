#!/usr/bin/env bash
# Render build script — installs Python dependencies only.
#
# No apt-get here: Render's native Python runtime runs the build as a non-root
# user without apt access, and it isn't needed anyway — PyMuPDF4LLM,
# faster-whisper (ctranslate2) and soundfile all ship prebuilt wheels.
set -o errexit

echo "Upgrading pip and build tools..."
pip install --upgrade pip setuptools wheel

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Build completed successfully!"
