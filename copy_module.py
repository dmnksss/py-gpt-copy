#!/usr/bin/env python3
import sys
import importlib
import importlib.util
import ast
from pathlib import Path
import logging

# Попытка импортировать pyperclip и установка, если отсутствует
try:
    import pyperclip
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyperclip"])
    import pyperclip


def find_project_root(start_path):
    """Detect project root by looking for dependency files"""
    markers = [
        'requirements.txt',
        'pyproject.toml',
        'Pipfile',
        'setup.py',
        '.git'
    ]

    current_path = Path(start_path).resolve()
    logger.debug(f"Starting project root search from: {current_path}")

    while True:
        logger.debug(f"Checking for markers in: {current_path}")
        for marker in markers:
            if (current_path / marker).exists():
                logger.info(f"Project root found at: {current_path} (contains {marker})")
                return current_path

        parent_path = current_path.parent
        if parent_path == current_path:
            logger.debug("Reached the filesystem root without finding project markers.")
            break
        current_path = parent_path

    logger.warning("Project root markers not found. Falling back to: "
                   f"{current_path} (deepest directory searched)")
    return current_path  # Fallback to deepest directory searched


def get_full_imports(file_path):
    """Parse AST to find all absolute and relative imports"""
    logger.debug(f"Parsing imports in file: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=str(file_path))
    except SyntaxError as e:
        logger.warning(f"Syntax error in {file_path}: {e}")
        return set()
    except Exception as e:
        logger.error(f"Failed to parse {file_path}: {e}")
        return set()

    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name)
                logger.debug(f"Found absolute import: {alias.name}")
        elif isinstance(node, ast.ImportFrom):
            module = node.module
            level = node.level
            if module:
                full_module = '.' * level + module
                imports.add(full_module)
                logger.debug(f"Found relative import with module: {full_module}")
            elif level > 0:
                relative_dots = '.' * level
                imports.add(relative_dots)
                logger.debug(f"Found relative import without module: {relative_dots}")
    logger.debug(f"Total imports found in {file_path}: {len(imports)}")
    return imports


def resolve_import_path(import_str, current_file, project_root):
    """Resolve import statement to absolute file path using importlib."""
    logger.debug(f"Resolving import '{import_str}' in {current_file}")

    try:
        # Attempt to find the module specification
        spec = importlib.util.find_spec(import_str)
        if spec is None:
            logger.debug(f"Module {import_str} not found by importlib.")
            return None

        if spec.origin is None:
            logger.debug(f"Module {import_str} has no origin.")
            return None

        module_path = Path(spec.origin).resolve()

        # Check if the module is within the project root
        try:
            module_path.relative_to(project_root)
            logger.debug(f"Module {import_str} resolved to {module_path}")
            return module_path
        except ValueError:
            logger.debug(f"Module {import_str} is external: {module_path}")
            return None

    except Exception as e:
        logger.error(f"Error resolving module {import_str}: {e}")
        return None


def collect_dependencies(start_path, project_root):
    """Recursively collect all project dependencies"""
    collected = set()
    to_process = [start_path.resolve()]
    logger.info(f"Starting dependency collection from: {start_path}")

    while to_process:
        current_file = to_process.pop()
        if current_file in collected:
            logger.debug(f"Already processed: {current_file}")
            continue

        collected.add(current_file)
        try:
            relative_current = current_file.relative_to(project_root)
        except ValueError:
            relative_current = current_file
        logger.info(f"🔍 Analyzing {relative_current}")

        imports = get_full_imports(current_file)

        for imp in imports:
            # Handle relative imports (start with '.')
            if imp.startswith('.'):
                # Convert relative import to absolute based on current_file
                levels = len(imp) - len(imp.lstrip('.'))
                relative_module = imp.lstrip('.')
                base_dir = current_file.parent
                logger.debug(f"Relative import: levels={levels}, relative_module='{relative_module}'")

                for _ in range(levels):
                    base_dir = base_dir.parent
                    logger.debug(f"Traversing up to: {base_dir}")

                if relative_module:
                    import_str = '.'.join([base_dir.relative_to(project_root).as_posix()] + relative_module.split('.'))
                else:
                    import_str = base_dir.relative_to(project_root).as_posix()

                logger.debug(f"Converted relative import to absolute: {import_str}")
            else:
                import_str = imp

            imp_path = resolve_import_path(import_str, current_file, project_root)
            if imp_path and imp_path.exists() and project_root in imp_path.parents:
                if imp_path not in collected:
                    logger.debug(f"Adding to processing queue: {imp_path}")
                    to_process.append(imp_path)
            else:
                logger.debug(f"Import '{imp}' in {current_file} is external or does not exist within the project.")

    logger.info(f"Dependency collection complete. Total files collected: {len(collected)}")
    return collected


def format_files(file_paths, project_root):
    """Format files into the required structure"""
    output = []
    logger.debug("Formatting collected files for clipboard output.")

    for path in sorted(file_paths):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Use forward slashes for consistency across platforms
                relative_path = path.relative_to(project_root)
                output.append(f"# {relative_path.as_posix()}\n{content}\n")
                logger.debug(f"Formatted file: {relative_path}")
        except Exception as e:
            logger.warning(f"⚠️ Skipping {path}: {str(e)}")

    total_lines = sum(len(content.splitlines()) + 1 for content in output)  # +1 for the header line
    logger.debug(f"Total lines to copy: {total_lines}")
    return '\n'.join(output)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Copy all imported project files recursively to clipboard.")
    parser.add_argument('module', help="Module name or path to the Python file.")
    parser.add_argument('--debug', action='store_true', help="Enable debug logging.")
    args = parser.parse_args()

    if args.debug:
        ch.setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled.")

    input_arg = args.module
    file_path = None
    project_root = None

    logger.debug(f"Received input argument: {input_arg}")

    if input_arg.endswith('.py') and Path(input_arg).exists():
        file_path = Path(input_arg).resolve()
        logger.debug(f"Input is a Python file: {file_path}")
        project_root = find_project_root(file_path.parent)
        sys.path.insert(0, str(project_root))
        logger.debug(f"Project root set to: {project_root}")
    else:
        try:
            logger.debug(f"Attempting to import module: {input_arg}")
            module = importlib.import_module(input_arg)
            file_path = Path(module.__file__).resolve()
            logger.debug(f"Module {input_arg} resolved to file: {file_path}")
            project_root = find_project_root(file_path.parent)
            sys.path.insert(0, str(project_root))
            logger.debug(f"Project root set to: {project_root}")
        except ModuleNotFoundError:
            logger.error(f"❌ Module not found: {input_arg}")
            sys.exit(1)
        except AttributeError:
            logger.error(f"❌ Unable to determine file path for module: {input_arg}")
            sys.exit(1)

    all_files = collect_dependencies(file_path, project_root)
    output = format_files(all_files, project_root)

    try:
        pyperclip.copy(output)
        logger.info(f"\n✅ Copied {len(all_files)} files:")
        for f in all_files:
            try:
                relative_path = f.relative_to(project_root)
            except ValueError:
                relative_path = f
            logger.info(f"  → {relative_path.as_posix()}")
        logger.info(f"📋 Total: {len(output.splitlines())} lines copied to clipboard")
    except pyperclip.PyperclipException:
        logger.error("❌ Clipboard access failed. Ensure that the necessary dependencies for pyperclip are installed.")
        # Optionally, you can print the output to stdout as a fallback
        logger.info("\n📄 Here is the copied content:\n")
        print(output)


if __name__ == "__main__":
    # Configure logging
    logger = logging.getLogger('copy_module')
    logger.setLevel(logging.DEBUG)  # Set to DEBUG to capture all levels of logs

    # Create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)  # Default log level; can be adjusted via command-line arguments

    # Create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(ch)

    main()