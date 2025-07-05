#!/bin/bash

# SudoThink Installation Script
# This script installs SudoThink to your system

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
INSTALL_DIR="$HOME/.sudothink"
SHELL_RC_FILE=""
SHELL_TYPE=""

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

    print_header() {
        echo -e "${BLUE}================================${NC}"
        echo -e "${BLUE}    SudoThink Installation${NC}"
        echo -e "${BLUE}================================${NC}"
    }

# Function to detect shell type
detect_shell() {
    if [[ -n "$ZSH_VERSION" ]]; then
        SHELL_TYPE="zsh"
        SHELL_RC_FILE="$HOME/.zshrc"
    elif [[ -n "$BASH_VERSION" ]]; then
        SHELL_TYPE="bash"
        SHELL_RC_FILE="$HOME/.bashrc"
    else
        print_error "Unsupported shell. Please use zsh or bash."
        exit 1
    fi
    print_status "Detected shell: $SHELL_TYPE"
}

# Function to check dependencies
check_dependencies() {
    print_status "Checking dependencies..."
    
    # Check if Python 3 is installed
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is required but not installed."
        print_status "Please install Python 3 and try again."
        exit 1
    fi
    
    # Check Python version
    PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    REQUIRED_VERSION="3.7"
    
    if python3 -c "import sys; exit(0 if sys.version_info >= (3, 7) else 1)"; then
        print_status "Python version: $PYTHON_VERSION ✓"
    else
        print_error "Python 3.7 or higher is required. Current version: $PYTHON_VERSION"
        exit 1
    fi
    
    # Check if pip is available
    if ! python3 -m pip --version &> /dev/null; then
        print_error "pip is required but not available."
        print_status "Please install pip and try again."
        exit 1
    fi
    
    print_status "All dependencies satisfied ✓"
}

# Function to install Python dependencies
install_python_deps() {
    print_status "Installing Python dependencies..."
    
    # Install required packages
    python3 -m pip install --user openai requests
    
    if [ $? -eq 0 ]; then
        print_status "Python dependencies installed successfully ✓"
    else
        print_error "Failed to install Python dependencies."
        exit 1
    fi
}

# Function to create installation directory
create_install_dir() {
    print_status "Creating installation directory..."
    
    if [[ -d "$INSTALL_DIR" ]]; then
        print_warning "Installation directory already exists: $INSTALL_DIR"
        read -p "Do you want to overwrite it? [y/N]: " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_status "Installation cancelled."
            exit 0
        fi
        rm -rf "$INSTALL_DIR"
    fi
    
    mkdir -p "$INSTALL_DIR"
    print_status "Installation directory created: $INSTALL_DIR"
}

# Function to copy files
copy_files() {
    print_status "Copying files..."
    
    # Copy the main script
    cp ai.py "$INSTALL_DIR/"
    chmod +x "$INSTALL_DIR/ai.py"
    
    # Copy the shell script
    cp ai.zsh "$INSTALL_DIR/"
    
    # Copy README
    cp README.md "$INSTALL_DIR/"
    
    # Copy LICENSE if it exists
    if [[ -f "LICENSE" ]]; then
        cp LICENSE "$INSTALL_DIR/"
    fi
    
    print_status "Files copied successfully ✓"
}

# Function to create shell configuration
setup_shell_config() {
    print_status "Setting up shell configuration..."
    
    # Check if already configured
    if grep -q "sudothink" "$SHELL_RC_FILE" 2>/dev/null; then
        print_warning "SudoThink is already configured in $SHELL_RC_FILE"
        read -p "Do you want to update the configuration? [y/N]: " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_status "Skipping shell configuration."
            return
        fi
        # Remove existing configuration
        sed -i.bak '/sudothink/d' "$SHELL_RC_FILE"
    fi
    
    # Add configuration to shell RC file
    echo "" >> "$SHELL_RC_FILE"
    echo "# SudoThink Configuration" >> "$SHELL_RC_FILE"
    echo "export SUDOTHINK_DIR=\"$INSTALL_DIR\"" >> "$SHELL_RC_FILE"
    echo "source \"$INSTALL_DIR/ai.zsh\"" >> "$SHELL_RC_FILE"
    
    print_status "Shell configuration added to $SHELL_RC_FILE ✓"
}

# Function to create uninstall script
create_uninstall_script() {
    cat > "$INSTALL_DIR/uninstall.sh" << 'EOF'
#!/bin/bash

# SudoThink Uninstall Script

set -e

INSTALL_DIR="$HOME/.sudothink"
SHELL_RC_FILE=""

# Detect shell
if [[ -n "$ZSH_VERSION" ]]; then
    SHELL_RC_FILE="$HOME/.zshrc"
elif [[ -n "$BASH_VERSION" ]]; then
    SHELL_RC_FILE="$HOME/.bashrc"
fi

echo "Uninstalling SudoThink..."

# Remove from shell configuration
if [[ -f "$SHELL_RC_FILE" ]]; then
    sed -i.bak '/sudothink/d' "$SHELL_RC_FILE"
    echo "Removed configuration from $SHELL_RC_FILE"
fi

# Remove installation directory
if [[ -d "$INSTALL_DIR" ]]; then
    rm -rf "$INSTALL_DIR"
    echo "Removed installation directory: $INSTALL_DIR"
fi

echo "SudoThink has been uninstalled successfully."
echo "Please restart your shell or run 'source $SHELL_RC_FILE' to apply changes."
EOF

    chmod +x "$INSTALL_DIR/uninstall.sh"
    print_status "Uninstall script created: $INSTALL_DIR/uninstall.sh"
}

# Function to create update script
create_update_script() {
    cat > "$INSTALL_DIR/update.sh" << 'EOF'
#!/bin/bash

# SudoThink Update Script

set -e

INSTALL_DIR="$HOME/.sudothink"
REPO_URL="https://github.com/yourusername/sudothink.git"
TEMP_DIR="/tmp/sudothink_update"

echo "Updating SudoThink..."

# Create temporary directory
mkdir -p "$TEMP_DIR"
cd "$TEMP_DIR"

# Clone the latest version
git clone "$REPO_URL" .

# Copy updated files
cp ai.py "$INSTALL_DIR/"
cp ai.zsh "$INSTALL_DIR/"
cp README.md "$INSTALL_DIR/"

# Clean up
cd /
rm -rf "$TEMP_DIR"

echo "SudoThink updated successfully!"
echo "Please restart your shell or run 'source ~/.zshrc' to apply changes."
EOF

    chmod +x "$INSTALL_DIR/update.sh"
    print_status "Update script created: $INSTALL_DIR/update.sh"
}

# Function to setup API key
setup_api_key() {
    print_status "Setting up OpenAI API key..."
    
    if [[ -n "$OPENAI_API_KEY" ]]; then
        print_status "OPENAI_API_KEY is already set in environment ✓"
    else
        print_warning "OPENAI_API_KEY is not set."
        echo "You can set it in several ways:"
        echo "1. Add to your shell configuration:"
        echo "   echo 'export OPENAI_API_KEY=\"your-key-here\"' >> $SHELL_RC_FILE"
        echo "2. Set it temporarily: export OPENAI_API_KEY=\"your-key-here\""
        echo "3. Create a .env file in the installation directory"
        
        read -p "Would you like to add it to your shell configuration now? [y/N]: " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            read -p "Enter your OpenAI API key: " api_key
            echo "export OPENAI_API_KEY=\"$api_key\"" >> "$SHELL_RC_FILE"
            print_status "API key added to $SHELL_RC_FILE"
        fi
    fi
}

# Function to create completion script
create_completion_script() {
    if [[ "$SHELL_TYPE" == "zsh" ]]; then
        cat > "$INSTALL_DIR/_ai" << 'EOF'
#compdef ai

_ai() {
    local curcontext="$curcontext" state line
    typeset -A opt_args

    _arguments -C \
        '1: :->mode' \
        '*: :->args'

    case $state in
        mode)
            local modes
            modes=(
                'plan:Generate a step-by-step plan'
                'explain:Explain a task or command'
                'chat:Start interactive chat mode'
            )
            _describe -t modes 'ai modes' modes
            ;;
        args)
            _files
            ;;
    esac
}

_ai "$@"
EOF
        print_status "Zsh completion script created: $INSTALL_DIR/_ai"
    fi
}

# Function to create version file
create_version_file() {
    cat > "$INSTALL_DIR/version" << 'EOF'
1.0.0
EOF
    print_status "Version file created"
}

# Function to test installation
test_installation() {
    print_status "Testing installation..."
    
    # Source the shell script
    source "$INSTALL_DIR/ai.zsh"
    
    # Test if ai function is available
    if type ai &> /dev/null; then
        print_status "Installation test successful ✓"
    else
        print_error "Installation test failed. ai function not found."
        exit 1
    fi
}

# Function to show post-installation instructions
show_post_install_instructions() {
    echo ""
    echo -e "${GREEN}================================${NC}"
    echo -e "${GREEN}    Installation Complete!${NC}"
    echo -e "${GREEN}================================${NC}"
    echo ""
    echo "SudoThink has been installed successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Set your OpenAI API key:"
    echo "   export OPENAI_API_KEY=\"your-key-here\""
    echo ""
    echo "2. Restart your shell or run:"
    echo "   source $SHELL_RC_FILE"
    echo ""
    echo "3. Start using SudoThink:"
    echo "   ai \"find all files larger than 100MB\""
    echo "   ai \"setup a new project\" plan"
    echo "   ai-chat"
    echo ""
    echo "Installation directory: $INSTALL_DIR"
    echo "Shell configuration: $SHELL_RC_FILE"
    echo ""
    echo "For more information, see: $INSTALL_DIR/README.md"
    echo ""
    echo "To uninstall, run: $INSTALL_DIR/uninstall.sh"
    echo "To update, run: $INSTALL_DIR/update.sh"
}

# Main installation function
main() {
    print_header
    
    # Check if running as root
    if [[ $EUID -eq 0 ]]; then
        print_error "Please do not run this script as root."
        exit 1
    fi
    
    detect_shell
    check_dependencies
    install_python_deps
    create_install_dir
    copy_files
    setup_shell_config
    create_uninstall_script
    create_update_script
    create_completion_script
    create_version_file
    setup_api_key
    test_installation
    show_post_install_instructions
}

# Run main function
main "$@"
