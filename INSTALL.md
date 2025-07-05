# SudoThink Installation Guide

This guide covers all the different ways to install SudoThink on various platforms.

## Prerequisites

- **Python 3.7 or higher**
- **OpenAI API key** (get one at [https://platform.openai.com/](https://platform.openai.com/))
- **zsh or bash shell**

## Installation Methods

### 1. Quick Install (Recommended)

The fastest way to get started:

```bash
curl -fsSL https://raw.githubusercontent.com/vusallyv/sudothink/main/install-oneline.sh | bash
```

This will:
- Download and run the installation script
- Install all dependencies
- Set up shell configuration
- Create necessary directories and files

### 2. Manual Installation

If you prefer to install manually:

```bash
# Clone the repository
git clone https://github.com/vusallyv/sudothink.git
cd sudothink

# Make installation script executable
chmod +x install.sh

# Run the installation
./install.sh
```

### 3. Python Package Installation

Install via pip:

```bash
pip install sudothink
```

Then manually set up shell integration:

```bash
# Download shell script
curl -fsSL https://raw.githubusercontent.com/vusallyv/sudothink/main/ai.zsh -o ~/.sudothink.zsh

# Add to your shell configuration
echo 'source ~/.sudothink.zsh' >> ~/.zshrc
```

### 4. Homebrew Installation (macOS)

```bash
# Add the tap
brew tap yourusername/sudothink

# Install SudoThink
brew install sudothink
```

### 5. Development Installation

For developers who want to contribute:

```bash
# Clone the repository
git clone https://github.com/vusallyv/sudothink.git
cd sudothink

# Install in development mode
pip install -e .

# Install development dependencies
pip install -e ".[dev]"

# Set up shell integration
chmod +x install.sh
./install.sh
```

## Platform-Specific Instructions

### macOS

1. **Install Homebrew** (if not already installed):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install sudothink**:
   ```bash
   brew install vusallyv/sudothink/sudothink
   ```

### Linux (Ubuntu/Debian)

1. **Install Python dependencies**:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   ```

2. **Install sudothink**:
   ```bash
   curl -fsSL https://raw.githubusercontent.com/vusallyv/sudothink/main/install-oneline.sh | bash
   ```

### Linux (CentOS/RHEL/Fedora)

1. **Install Python dependencies**:
   ```bash
   # CentOS/RHEL
   sudo yum install python3 python3-pip

   # Fedora
   sudo dnf install python3 python3-pip
   ```

2. **Install sudothink**:
   ```bash
   curl -fsSL https://raw.githubusercontent.com/vusallyv/sudothink/main/install-oneline.sh | bash
   ```

### Windows (WSL)

1. **Install WSL** (if not already installed):
   ```powershell
   wsl --install
   ```

2. **Install sudothink in WSL**:
   ```bash
   curl -fsSL https://raw.githubusercontent.com/vusallyv/sudothink/main/install-oneline.sh | bash
   ```

## Configuration

### Setting up OpenAI API Key

1. **Get an API key**:
   - Visit [https://platform.openai.com/](https://platform.openai.com/)
   - Sign up or log in
   - Go to API Keys section
   - Create a new API key

2. **Set the API key**:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

3. **Make it permanent**:
   ```bash
   echo 'export OPENAI_API_KEY="your-api-key-here"' >> ~/.zshrc
   source ~/.zshrc
   ```

### Shell Configuration

The installation script automatically configures your shell, but you can also do it manually:

```bash
# For zsh
echo 'source ~/.sudothink/ai.zsh' >> ~/.zshrc

# For bash
echo 'source ~/.sudothink/ai.zsh' >> ~/.bashrc
```

## Verification

After installation, verify that everything is working:

```bash
# Check if ai function is available
type ai

# Test with a simple command
ai "echo hello world"

# Test different modes
ai "explain what ls -la does" explain
ai "setup a test directory" plan
```

## Troubleshooting

### Common Issues

**"OPENAI_API_KEY not set"**
```bash
export OPENAI_API_KEY="your-key-here"
```

**"Python 3 not found"**
```bash
# macOS
brew install python3

# Ubuntu/Debian
sudo apt install python3

# CentOS/RHEL
sudo yum install python3
```

**"Permission denied"**
```bash
chmod +x install.sh
```

**"Command not found: ai"**
```bash
source ~/.zshrc
# or
source ~/.bashrc
```

### Uninstallation

To uninstall sudothink:

```bash
# If installed via install script
~/.sudothink/uninstall.sh

# If installed via pip
pip uninstall sudothink

# If installed via Homebrew
brew uninstall sudothink
```

### Updating

To update sudothink:

```bash
# If installed via install script
~/.sudothink/update.sh

# If installed via pip
pip install --upgrade sudothink

# If installed via Homebrew
brew upgrade sudothink
```

## Support

If you encounter any issues:

1. Check the [troubleshooting section](#troubleshooting)
2. Search [existing issues](https://github.com/vusallyv/sudothink/issues)
3. Create a [new issue](https://github.com/vusallyv/sudothink/issues/new)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for information on how to contribute to the project. 