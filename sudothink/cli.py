#!/usr/bin/env python3
"""
Command-line interface for SudoThink
"""

import sys
from .assistant import AITerminalAssistant

def main():
    """Main CLI entry point"""
    if len(sys.argv) < 2:
        print("❌ Usage: sudothink <query> [mode]")
        print("Modes: command (default), plan, explain")
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