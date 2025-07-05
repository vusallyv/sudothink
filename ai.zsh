function ai() {
    # Check if OpenAI API key is set
    if [[ -z "$OPENAI_API_KEY" ]]; then
        echo "❌ OPENAI_API_KEY not set."
        return 1
    fi
    
    input="$*"
    command=$(python3 ~/.ai-terminal-plugin/ai.py "$input")
    
    # Check if the command was successfully generated (not an error message)
    if [[ $? -ne 0 ]] || [[ "$command" == *"❌"* ]]; then
        echo "$command"
        return 1
    fi
    
    echo "\n🤖 Suggested command:"
    echo "$command"
    echo -n "\n🚀 Run this command? [y/N]: "
    read ans
    if [[ "$ans" == "y" || "$ans" == "Y" ]]; then
        eval "$command"
    fi
}

alias #ai='ai'
