#!/usr/bin/env python3
"""
SudoThink - Backward compatibility script
This script maintains compatibility with the original installation method
"""

import sys
import os

# Add the current directory to the path so we can import the package
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from sudothink.cli import main
except ImportError:
    # Fallback to the old implementation if package is not available
    from sudothink.assistant import AITerminalAssistant
    
    def main():
        """Main CLI entry point"""
        if len(sys.argv) < 2:
            print("❌ Usage: ai.py <query> [mode]")
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
