function ai() {
    # Check if OpenAI API key is set
    if [[ -z "$OPENAI_API_KEY" ]]; then
        echo "❌ OPENAI_API_KEY not set."
        return 1
    fi
    
    # Parse arguments for mode
    local mode="command"
    local query=""
    
    # Check if last argument is a mode
    if [[ "${@: -1}" == "plan" || "${@: -1}" == "explain" ]]; then
        mode="${@: -1}"
        query="${@:1:$(($#-1))}"
    else
        query="$*"
    fi
    
    # Handle different modes
    if [[ "$mode" == "plan" ]]; then
        echo "📋 Generating step-by-step plan..."
        python3 "$SUDOTHINK_DIR/ai.py" "$query" plan
        return $?
    elif [[ "$mode" == "explain" ]]; then
        echo "💡 Analyzing request..."
        python3 "$SUDOTHINK_DIR/ai.py" "$query" explain
        return $?
    fi
    
    # Default command mode
    local command=$(python3 "$SUDOTHINK_DIR/ai.py" "$query")
    
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
        # Run the command and capture any error output
        error_output=$(eval "$command" 2>&1)
        exit_code=$?
        
        # If command failed, retry with the error message
        if [[ $exit_code -ne 0 ]]; then
            echo "\n❌ Command failed with error:"
            echo "$error_output"
            echo -n "\n🔄 Retry with corrected command? [y/N]: "
            read retry_ans
            if [[ "$retry_ans" == "y" || "$retry_ans" == "Y" ]]; then
                # Create a new request with the original input and error message
                retry_input="$query. The previous command failed with error: $error_output. Please provide a corrected command that works on this system."
                corrected_command=$(python3 "$SUDOTHINK_DIR/ai.py" "$retry_input")
                
                # Check if the corrected command was successfully generated
                if [[ $? -eq 0 ]] && [[ "$corrected_command" != *"❌"* ]]; then
                    echo "\n🤖 Corrected command:"
                    echo "$corrected_command"
                    echo -n "\n🚀 Run the corrected command? [y/N]: "
                    read corrected_ans
                    if [[ "$corrected_ans" == "y" || "$corrected_ans" == "Y" ]]; then
                        eval "$corrected_command"
                    fi
                else
                    echo "$corrected_command"
                fi
            fi
        else
            # Command succeeded, show output if any
            if [[ -n "$error_output" ]]; then
                echo "$error_output"
            fi
        fi
    fi
}

# Helper functions for different modes
function ai-plan() {
    ai "$*" plan
}

function ai-explain() {
    ai "$*" explain
}

# Interactive mode for complex conversations
function ai-chat() {
    echo "💬 AI Terminal Chat Mode"
    echo "Type 'exit' to quit, 'help' for commands"
    
    while true; do
        echo -n "\n🤖 You: "
        read -r user_input
        
        if [[ "$user_input" == "exit" ]]; then
            echo "👋 Goodbye!"
            break
        elif [[ "$user_input" == "help" ]]; then
            echo "Available commands:"
            echo "  exit - Exit chat mode"
            echo "  help - Show this help"
            echo "  plan <task> - Generate a plan for a task"
            echo "  explain <task> - Explain a task"
            continue
        elif [[ "$user_input" =~ ^plan\ (.+)$ ]]; then
            ai-plan "${BASH_REMATCH[1]}"
        elif [[ "$user_input" =~ ^explain\ (.+)$ ]]; then
            ai-explain "${BASH_REMATCH[1]}"
        else
            ai "$user_input"
        fi
    done
}

# Alias for the main function
alias #ai='ai'
