#!/bin/bash

mkdir -p ~/.ai-terminal-plugin
cp ai.py ~/.ai-terminal-plugin/
cp ai.zsh ~/.ai-terminal-plugin/

if ! grep -q "source ~/.ai-terminal-plugin/ai.zsh" ~/.zshrc; then
    echo "source ~/.ai-terminal-plugin/ai.zsh" >> ~/.zshrc
    echo "✅ Added plugin to ~/.zshrc"
else
    echo "ℹ️ Plugin already sourced in ~/.zshrc"
fi

echo "✅ Installed successfully. Restart your terminal or run 'source ~/.zshrc'"
