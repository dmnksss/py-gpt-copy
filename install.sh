#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Function to display informational messages
function echo_info() {
    echo -e "\033[1;32m[INFO]\033[0m $1"
}

function echo_error() {
    echo -e "\033[1;31m[ERROR]\033[0m $1" >&2
}

# Check for Python3 installation
if ! command -v python3 &> /dev/null
then
    echo_error "Python3 is not installed. Please install Python3 and try again."
    exit 1
fi

# Check for pip3 installation
if ! command -v pip3 &> /dev/null
then
    echo_info "pip3 not found. Attempting to install pip3."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py --user
    export PATH="$HOME/.local/bin:$PATH"
    if ! command -v pip3 &> /dev/null
    then
        echo_error "Failed to install pip3. Please install pip3 manually."
        exit 1
    fi
    rm get-pip.py
fi

# Install necessary system dependencies for pyperclip (for Linux)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if ! command -v xclip &> /dev/null && ! command -v xsel &> /dev/null
    then
        echo_info "Installing xclip for clipboard support on Linux."
        sudo apt-get update
        sudo apt-get install -y xclip || sudo yum install -y xclip || sudo pacman -S --noconfirm xclip
    fi
fi

# Define installation directory
INSTALL_DIR="/usr/local/lib/python3$(python3 -c 'import sys; print(sys.version_info.major)')/dist-packages/copy_module"

# Clone the repository
TEMP_DIR=$(mktemp -d)
echo_info "Downloading copy-module script from the repository..."
git clone https://github.com/your_username/copy-module.git "$TEMP_DIR"

# Navigate to the project directory
cd "$TEMP_DIR"

# Install the package globally
echo_info "Installing copy-module globally..."
sudo pip3 install .

# Clean up the temporary directory
cd ~
rm -rf "$TEMP_DIR"

echo_info "copy-module has been successfully installed and is available globally!"
echo_info "You can run it using the command: copy-module"