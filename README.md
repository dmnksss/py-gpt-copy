# py-gpt-copy

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-APACHE-yellow.svg)](LICENSE)

`py-gpt-copy` is a command-line utility that recursively gathers all imported project files and copies their combined contents to your clipboard. This makes it easy to share your module’s dependencies—perfect for generating well-mocked tests, debugging complex import structures, or sharing code with AI assistants like ChatGPT.

---

## Table of Contents

- [Features](#features)
- [Use Cases](#use-cases)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Development](#development)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Recursive Analysis:** Scans your module or Python file to identify all imported files within the project.
- **Automated Dependency Resolution:** Uses Python’s AST and importlib to resolve both absolute and relative imports.
- **Clipboard Integration:** Combines file contents (with file headers) and copies them to your clipboard.
- **Detailed Logging:** Optionally enable debug logging to trace the dependency collection process.
- **Project Root Detection:** Automatically identifies the project root by looking for standard markers (e.g., `requirements.txt`, `.git`, etc.).

---

## Use Cases

- **Sharing Code with AI:** Easily copy all dependencies to share with ChatGPT or other AI tools to generate unit tests, mocks, or refactor code.
- **Dependency Debugging:** Quickly analyze and debug complex import structures in large projects.
- **Documentation:** Generate a consolidated view of a module’s dependencies for documentation or code reviews.
- **Project Analysis:** Understand the structure of your project by visualizing which files are interconnected.

---

## Installation

### Prerequisites

- **Python 3.6 or higher**
- **pip:** To install required packages

### Global Installation via Installation Script

Install `py-gpt-copy` globally by running the following command in your terminal:

```bash
sudo curl -L https://raw.githubusercontent.com/dmnksss/py-gpt-copy/refs/heads/main/copy_module.py -o /usr/local/bin/py-gpt-copy && sudo chmod +x /usr/local/bin/py-gpt-copy
```

Verify the installation:

```bash
which py-gpt-copy
```

---

## Usage

Once installed, use the command-line tool as follows:

```bash
py-gpt-copy <module_name_or_path> [--debug]
```

- **`<module_name_or_path>`**: Name of the module or the path to a Python file.
- **`--debug`**: *(Optional)* Enable detailed logging for troubleshooting.

### Examples

- **Copy dependencies by module name:**

    ```bash
    py-gpt-copy my_module
    ```

- **Copy dependencies by file path:**

    ```bash
    py-gpt-copy path/to/my_module.py
    ```

- **Enable debug logging:**

    ```bash
    py-gpt-copy my_module --debug
    ```

After execution, the tool will analyze the file, recursively gather all imported files within the project, format them with file headers, and copy the combined content to your clipboard.

#### Sample Output

```
2025-01-31 14:30:05,000 - INFO - 
✅ Copied 5 files:
  → client/domain/service/task_logger.py
  → client/domain/usecase/log_task_status.py
  → client/domain/service/__init__.py
  → client/domain/usecase/__init__.py
📋 Total: 200 lines copied to clipboard
```

---

## How It Works

1. **Project Root Detection:**  
   The script starts by identifying the project root directory using markers like `requirements.txt`, `setup.py`, or `.git`.

2. **Parsing Imports:**  
   It uses Python’s `ast` module to parse the target file and extract both absolute and relative imports.

3. **Resolving Paths:**  
   Using `importlib`, it resolves each import to its absolute file path—ensuring that only files within the project are processed.

4. **Recursive Collection:**  
   The script recursively collects all dependencies, avoiding duplicates and external modules.

5. **Formatting & Clipboard:**  
   Each file’s content is prefixed with its relative file path and all contents are concatenated before being copied to the clipboard using `pyperclip`.

For a detailed look at the implementation, check out the [source code](#).

---

## Development

### Setting Up a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Installing Development Dependencies

```bash
pip install -e .
```

### Running Locally

After setting up, you can run the script directly:

```bash
./copy_module.py <module_name_or_path> [--debug]
```

---

## Testing

Place your tests in the `tests/` directory. Run tests using your preferred testing framework, such as `unittest`:

```bash
python -m unittest discover tests
```

---

## Troubleshooting

- **Clipboard Issues:**  
  If you encounter clipboard errors, ensure that all dependencies for `pyperclip` are installed or consider printing the output to stdout as a fallback.

- **Module Not Found Errors:**  
  Verify that the module or file path you provided exists and that your project has the necessary dependency markers.

For additional help, please [open an issue](https://github.com/dmnksss/py-gpt-copy/issues).