# Python Development in SkogAI

## SkogAI Python Project Configuration

### Project Initialization
When setting up a new Python project within SkogAI, we use `uv` for project initialization. This tool helps streamline the setup process, ensuring all projects adhere to our standardized configuration.

### Example: SkogCLI Project Setup
For instance, when initializing the `SkogCLI` project, we executed the following command:
```bash
uv init --app --name skogcli --build-backend flit --python 3.13 --no-readme --directory /home/skogix/.skogai/projects/skogcli/
```
This command sets up the project with `flit` as the build backend and specifies Python 3.13 as the required Python version.

### pyproject.toml Configuration
After initialization, a `pyproject.toml` file is created in the project directory with the following configuration:

```toml
[project]
name = "skogcli"
version = "0.1.0"
description = "Add your description here"
authors = [
    { name = "Emil Skogsund", email = "emil.skogsund@gmail.com" }
]
requires-python = ">=3.13"
dependencies = []

[project.scripts]
skogcli = "skogcli:main"

[build-system]
requires = ["flit_core>=3.2,<4"]
build-backend = "flit_core.buildapi"
```

This file defines the project's metadata, including the name, version, description, author details, and the required Python version. It also specifies the project's dependencies, entry points for scripts, and the build system requirements.

### Project Structure
The project structure includes a `src` directory with a `skogcli` module, which contains an `__init__.py` file. This setup is typical for Python packages intended for distribution.

## Virtual Environment and Dependency Management

### Activating the Virtual Environment
After setting up the project, a virtual environment is created using `uv venv`. To activate this environment automatically when entering the project directory, `direnv` is used with the following setup in `.envrc`:

```bash
source .venv/bin/activate
```

Running `which python` or `which pip` in the terminal will confirm that the active binaries are being used from `.venv/bin/`, indicating that the virtual environment is active.

### Managing Dependencies
To add dependencies to the project, use the following `uv` commands:

- To install a new package, e.g., Flask:
  ```bash
  uv pip install flask
  ```
- To add the package to the project's dependency list and synchronize the environment:
  ```bash
  uv add flask && uv lock && uv sync
  ```

These steps ensure that all dependencies are properly managed and the environment is prepared for production.

## Conclusion
This section outlines the standard practices for setting up Python projects at SkogAI, ensuring consistency and adherence to best practices across all our Python-based projects, including environment management and dependency handling.
