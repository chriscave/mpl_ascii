# Contributing to `mpl_ascii`

Thank you for your interest in contributing to `mpl_ascii`! Here are some guidelines to help you get started.

## Pull Requests

- **Fork the Repository**: Please make PRs from your own fork of the repository.

## Setting Up Your Environment

- **pyenv**: We use pyenv to manage multiple Python versions. Ensure you have pyenv installed and set up before proceeding.
- **Creating Virtual Environments**: You can create virtual environments using venv with the following commands:

```bash
make venv-dev
make venv-3.7
make venv-3.8
```

## Running Tests and Examples

- **make accept**: This command runs all example plots and saves the figures to text files. Ensure you run make accept and commit the resulting text files as the last step before submitting your PR. This ensures the example text files are up to date with the current state of the code and prevents build failures.

## Adding New Plots

- **Example Programs**: New plots should come with a Python program demonstrating the plot. These programs should be placed in the examples folder.

- **Template**: Each example program follows this template:

```python
import matplotlib
matplotlib.use('mpl_ascii')
import matplotlib.pyplot as plt

if __name__ == "__main__":
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--out", type=str)

    args = parser.parse_args()
    out = args.out

    fig, ax = plt.subplots()

    # Your plotting code here

    if out:
        fig.savefig(out)

    plt.show()
```

- **Running Examples**: To run and save the example plot, use the command:

```bash
make name_of_program.txt
```
This will save the text file to the examples folder.

## Summary

1. 🏗️ Fork the repository.
1. 🐍 Use pyenv to manage Python versions.
1. 📦 Create virtual environments with make venv-dev, make venv-3.7, make venv-3.8, etc.
1. 📁 Place new example programs in the examples folder, following the provided template.
1. 🛠️ Run new examples with make name_of_example.txt.
1. ✅ Run make accept and commit the resulting text files as the last step before submitting your PR to ensure the example text files are up to date and to prevent build failures.

Thank you for contributing!