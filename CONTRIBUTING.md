# Contributing to `mpl_ascii`

Thank you for your interest in contributing to `mpl_ascii`! Here are some guidelines to help you get started.

## Project Goals

This repository is designed around four core principles:

- **Accessible**: The ASCII output should work across different terminals and environments, requiring no special dependencies beyond Python
- **Seamless**: Users should be able to drop in the backend with minimal code changes (`matplotlib.use('mpl_ascii')`) and get meaningful output
- **Scalable**: The architecture should handle complex matplotlib figures with multiple artists and elements efficiently
- **Contributor-friendly**: Adding support for new matplotlib artists should be straightforward with clear patterns to follow

## Pull Requests

- **Fork the Repository**: Please make PRs from your own fork of the repository.

## Setting Up Your Environment

- **pyenv**: We use pyenv to manage multiple Python versions. Ensure you have pyenv installed and set up before proceeding.
- **Creating Virtual Environments**: You can create virtual environments using venv with the following commands:

```bash
make venv-dev
make venv-3.9
make venv-3.10
```

## Running Tests and Examples

- **make accept**: This command runs all example plots and saves the figures to text files. Ensure you run make accept and commit the resulting text files as the last step before submitting your PR. This ensures the example text files are up to date with the current state of the code and prevents build failures.

## Summary

1. 🏗️ Fork the repository.
1. 🐍 Use pyenv to manage Python versions.
1. 📦 Create virtual environments with make venv-dev, make venv-3.7, make venv-3.8, etc.
1. ✅ Run make accept and commit the resulting text files as the last step before submitting your PR to ensure the example text files are up to date and to prevent build failures.

Thank you for contributing!