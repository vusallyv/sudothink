# SudoThink - Advanced AI Terminal Assistant

An intelligent terminal assistant that uses OpenAI's GPT-4 to help you with complex shell tasks, from simple commands to multi-step workflows.

## Features

### 🚀 Core Capabilities
- **Smart Command Generation**: Convert natural language to shell commands
- **Multi-Step Task Planning**: Break down complex tasks into executable steps
- **Context Awareness**: Understands your system, current directory, and recent commands
- **Automatic Error Recovery**: Retry failed commands with error context
- **Interactive Chat Mode**: Have conversations with the AI assistant

### 🎯 Multiple Modes

#### 1. Command Mode (Default)
Generate and execute single shell commands:
```bash
ai "find all files larger than 100MB"
ai "show me the top 10 processes by memory usage"
```

#### 2. Plan Mode
Generate step-by-step plans for complex tasks:
```bash
ai "setup a new Python project with virtual environment" plan
ai "backup my documents and sync to cloud storage" plan
```

#### 3. Explain Mode
Get explanations and analysis of tasks:
```bash
ai "what does this command do: docker-compose up -d" explain
ai "how to optimize my system performance" explain
```

#### 4. Interactive Chat Mode
Have ongoing conversations:
```bash
ai-chat
```

### 🔧 Advanced Features

#### Context Awareness
- **System Information**: OS, shell, current directory, available commands
- **Command History**: Learns from your recent commands
- **Directory Structure**: Understands your current workspace
- **Persistent Context**: Remembers previous interactions

#### Smart Error Handling
- **Automatic Retry**: When commands fail, automatically generates corrected versions
- **Error Analysis**: Includes error messages in retry requests
- **Step-by-Step Recovery**: For complex tasks, can retry individual steps

#### Multi-Step Execution
- **Interactive Steps**: Review and approve each step before execution
- **Skip Options**: Skip steps that aren't needed
- **Retry Logic**: Retry failed steps individually
- **Progress Tracking**: Clear indication of current step and progress

## Installation

### Quick Install (Recommended)

**One-liner installation:**
```bash
curl -fsSL https://raw.githubusercontent.com/vusallyv/sudothink/master/install-oneline.sh | bash
```

**Manual installation:**
```bash
git clone https://github.com/vusallyv/sudothink.git
cd sudothink
chmod +x install.sh
./install.sh
```

### Alternative Installation Methods

#### Via pip (Python package)
```bash
pip install sudothink
```

**Note:** The pip package will be available after publishing to PyPI. For now, use the one-liner or manual installation methods.

#### Via Homebrew (macOS)
```bash
# Add to your tap first
brew tap yourusername/sudothink
brew install sudothink
```

**Note:** Homebrew installation requires the tap to be published first. For now, use the one-liner or manual installation methods.

### Setup

#### Option 1: One-time Configuration (Recommended)
Configure your API key once and it will be remembered:

```bash
ai setup
```

This will prompt you to enter your OpenAI API key securely. The key will be stored in `~/.sudothink/config.json` with restricted permissions.

#### Option 2: Environment Variable (Traditional)
Set up your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY="your-api-key-here"
```

**Add to your shell profile** (if not done automatically):
```bash
echo 'export OPENAI_API_KEY="your-api-key-here"' >> ~/.zshrc
source ~/.zshrc
```

#### Setup Commands
```bash
ai setup                    # Configure API key (interactive)
ai setup --api-key "sk-..." # Configure API key (non-interactive)
ai setup --status          # Check configuration status
ai setup --remove          # Remove stored API key
```

## Usage Examples

### Simple Commands
```bash
# Find files
ai "find all PDF files in my documents folder"

# System monitoring
ai "show me disk usage for all mounted drives"

# Process management
ai "kill all processes using more than 1GB of memory"
```

### Complex Tasks
```bash
# Multi-step setup
ai "setup a new Node.js project with TypeScript, ESLint, and Prettier" plan

# Data processing
ai "download a CSV file, process it with Python, and generate a report" plan

# System maintenance
ai "clean up old log files, update packages, and restart services" plan
```

### Learning and Analysis
```bash
# Understand commands
ai "explain what 'docker-compose up -d' does" explain

# Get recommendations
ai "how can I improve my shell productivity" explain

# Debug issues
ai "my Python script is running slowly, help me optimize it" explain
```

### Interactive Mode
```bash
ai-chat

# In chat mode:
🤖 You: plan setup a web server
🤖 You: explain what nginx does
🤖 You: find files modified today
🤖 You: exit
```

## Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `AI_TRUST_MODE`: Set to "true" to run commands without confirmation (use with caution)

### Files Created
- `~/.sudothink/config.json`: API key and configuration (secure, owner-only permissions)
- `~/.ai-terminal-context.json`: Persistent context and settings
- `~/.ai-terminal-history.log`: Interaction history for learning

## Safety Features

### Command Confirmation
- All commands require explicit confirmation before execution
- Clear display of what command will be run
- Option to skip or modify commands

### Error Handling
- Automatic detection of command failures
- Smart retry with error context
- Graceful handling of API errors

### Context Limits
- Directory structure limited to prevent overwhelming
- Command history limited to recent entries
- File size limits on generated content

## Advanced Usage

### Custom Prompts
You can modify the system prompts in `ai.py` to customize the AI's behavior:

```python
# In the generate_response method, modify the prompt templates
if mode == "command":
    prompt += """
    YOUR CUSTOM INSTRUCTIONS HERE
    """
```

### Extending Functionality
The modular design makes it easy to add new modes:

1. Add a new mode to the `generate_response` method
2. Update the argument parsing in `main()`
3. Add corresponding shell function in `ai.zsh`

### Integration with Other Tools
- **Git Integration**: Use with git workflows
- **Docker Support**: Container management commands
- **Cloud Services**: AWS, GCP, Azure commands
- **Development Tools**: IDE integration, build systems

## Troubleshooting

### Common Issues

**"OpenAI API key not configured"**
```bash
# Option 1: One-time setup (recommended)
ai setup

# Option 2: Set environment variable
export OPENAI_API_KEY="your-key-here"
```

**Command not found**
- The AI will automatically retry with corrected commands
- Use `explain` mode to understand what went wrong

**Permission denied**
- Check file permissions
- Use `sudo` when appropriate (the AI will suggest this)

### Debug Mode
For troubleshooting, you can run the Python script directly:
```bash
python3 ai.py "your query" [mode]
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with OpenAI's GPT-4 API
- Inspired by modern CLI tools and AI assistants
- Designed for developer productivity and system administration