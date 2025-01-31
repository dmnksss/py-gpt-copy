
# copy-module

`copy-module` is a command-line utility that recursively copies all imported project files and places their combined contents into the clipboard.
It can be helpful when you need to share a module’s dependencies with chatgpt or other AI to generate well mocked tests.

## Installation

### Prerequisites

- Python 3.6 or higher
- `pip` for installing packages

### Global Installation via Installation Script

For convenient global installation of `copy-module` on your system, follow these steps:

1. **Download and Run the Installation Script:**

Open your terminal and execute the following command:

```bash
   wget -O - https://raw.githubusercontent.com/your_username/copy-module/main/install.sh | bash
````
Explanation:
- wget -O -: Downloads the file and outputs it to standard output.
- ash: Pipes the downloaded script to the bash interpreter for execution.
2. Permission Prompt:
The script may prompt you for your password to gain sudo privileges required for installing global packages and system dependencies.

3. Verify Installation:
After installation, ensure that the copy-module command is available:

```bash
which copy-module
```

Expected output:

```bash
/usr/local/bin/copy-module
```

## Usage

After installation, you can use the copy-module command in your terminal.

Syntax

```bash
copy-module <module_name_or_path> [--debug]

	•	<module_name_or_path>: The name of the module or the path to the Python file whose dependencies you want to copy.
	•	--debug: (Optional) Enables detailed logging for debugging purposes.
```

### Examples

1. Copying Dependencies by Module Name:

```bash
copy-module my_module
```

2.	Copying Dependencies by File Path:

```bash
copy-module path/to/my_module.py
```

3.	Enabling Detailed Logging:

```bash
copy-module my_module --debug
```


### What Happens
- The script analyzes the specified module or file.
- Recursively gathers all imported files within the project’s root directory.
- Combines the contents of all found files, prefixing each with comments indicating their paths.
- Copies the combined content to the clipboard.
- Displays a list of copied files and the total number of lines.

Sample Output

```
2025-01-31 14:30:05,000 - INFO - 
✅ Copied 5 files:
  → client/domain/service/task_logger.py
  → client/domain/usecase/log_task_status.py
  → client/domain/service/__init__.py
  → client/domain/usecase/__init__.py
📋 Total: 200 lines copied to clipboard
```

## Testing

You can add tests to the tests/ directory and run them using unittest or another testing framework.

## Development
1.	Creating a Virtual Environment:

```bash
python3 -m venv venv
source venv/bin/activate
```
2.	Installing Development Dependencies:
```bash
pip install -e .
```


## Troubleshooting

If you encounter issues or have questions, please open an issue in the repository or contact the author.
