#!/usr/bin/env python3
"""
Command-line interface for SudoThink
"""

import sys
import argparse
from .assistant import AITerminalAssistant
from .setup import main as setup_main

def main():
    """Main CLI entry point"""
    # Check for setup command
    if len(sys.argv) > 1 and sys.argv[1] == "setup":
        # Remove 'setup' from argv and pass to setup module
        sys.argv.pop(1)
        setup_main()
        return
    
    # Check for help on setup
    if len(sys.argv) > 1 and sys.argv[1] in ["--help", "-h"]:
        print("SudoThink - AI Terminal Assistant")
        print("\nUsage:")
        print("  sudothink <query> [mode]     - Generate command or plan")
        print("  sudothink setup              - Configure API key")
        print("  sudothink setup --status     - Show configuration status")
        print("  sudothink setup --remove     - Remove stored API key")
        print("\nModes: command (default), plan, explain")
        return
    
    if len(sys.argv) < 2:
        print("❌ Usage: sudothink <query> [mode]")
        print("Modes: command (default), plan, explain")
        print("Run 'sudothink setup' to configure your API key")
        sys.exit(1)
    
    query = " ".join(sys.argv[1:-1]) if len(sys.argv) > 2 else " ".join(sys.argv[1:])
    mode = sys.argv[-1] if len(sys.argv) > 2 and sys.argv[-1] in ["command", "plan", "explain"] else "command"
    
    assistant = AITerminalAssistant()
    
    # Analyze task complexity
    is_complex = assistant.analyze_task_complexity(query)
    
    if is_complex and mode == "command":
        print("🤔 This appears to be a complex task. Consider using 'plan' mode for multi-step execution.")
        response = input("🔄 Generate a plan instead? [y/N]: ").lower()
        if response == 'y':
            mode = "plan"
    
    if mode == "plan":
        print("📋 Generating step-by-step plan...")
        plan = assistant.generate_response(query, mode="plan")
        print(f"\n📋 Plan:\n{plan}")
        
        response = input("\n🚀 Execute this plan? [y/N]: ").lower()
        if response == 'y':
            assistant.execute_multi_step_plan(plan)
    elif mode == "explain":
        print("💡 Analyzing request...")
        explanation = assistant.generate_response(query, mode="explain")
        print(f"\n💡 Analysis:\n{explanation}")
    else:
        # Default command mode
        command = assistant.generate_response(query, mode="command")
        print(command)

if __name__ == "__main__":
    main() 