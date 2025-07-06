#!/usr/bin/env python3
import os
import sys
import subprocess
import json
import platform
from datetime import datetime
from openai import OpenAI, AuthenticationError
from .config import Config

class AITerminalAssistant:
    def __init__(self):
        self.config = Config()
        self.api_key = self.config.get_api_key()
        
        if not self.api_key:
            print("❌ OpenAI API key not configured.")
            print("💡 Run 'ai-setup' to configure your API key once, or set OPENAI_API_KEY environment variable.")
            sys.exit(1)
        
        self.client = OpenAI(api_key=self.api_key)
        self.context_file = os.path.expanduser("~/.ai-terminal-context.json")
        self.history_file = os.path.expanduser("~/.ai-terminal-history.log")
        
    def get_system_info(self):
        """Gather comprehensive system information"""
        info = {
            "os": platform.system(),
            "os_version": platform.release(),
            "shell": os.getenv("SHELL", "unknown"),
            "current_dir": os.getcwd(),
            "user": os.getenv("USER", "unknown"),
            "home": os.path.expanduser("~"),
            "available_commands": self.get_available_commands()
        }
        
        # Get directory structure (limited depth to avoid overwhelming)
        try:
            tree_output = subprocess.run(["find", ".", "-maxdepth", "2", "-type", "d"], 
                                       capture_output=True, text=True, timeout=5)
            info["directory_structure"] = tree_output.stdout[:1000]  # Limit size
        except:
            info["directory_structure"] = "Unable to get directory structure"
            
        return info
    
    def get_available_commands(self):
        """Get list of available commands in PATH"""
        try:
            path_dirs = os.getenv("PATH", "").split(":")
            commands = set()
            for path_dir in path_dirs:
                if os.path.exists(path_dir):
                    try:
                        for file in os.listdir(path_dir):
                            if os.access(os.path.join(path_dir, file), os.X_OK):
                                commands.add(file)
                    except:
                        continue
            return list(commands)[:50]  # Limit to first 50
        except:
            return []
    
    def get_recent_commands(self, limit=10):
        """Get recent commands from shell history"""
        try:
            # Try to get from various shell history files
            history_files = [
                os.path.expanduser("~/.zsh_history"),
                os.path.expanduser("~/.bash_history"),
                os.path.expanduser("~/.history")
            ]
            
            for hist_file in history_files:
                if os.path.exists(hist_file):
                    with open(hist_file, 'r', errors='ignore') as f:
                        lines = f.readlines()
                        return [line.strip() for line in lines[-limit:] if line.strip()]
        except:
            pass
        return []
    
    def load_context(self):
        """Load previous context if available"""
        try:
            if os.path.exists(self.context_file):
                with open(self.context_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        return {}
    
    def save_context(self, context):
        """Save current context"""
        try:
            with open(self.context_file, 'w') as f:
                json.dump(context, f, indent=2)
        except:
            pass
    
    def log_interaction(self, query, response, success=True):
        """Log the interaction for learning"""
        try:
            with open(self.history_file, 'a') as f:
                timestamp = datetime.now().isoformat()
                f.write(f"[{timestamp}] Query: {query}\n")
                f.write(f"[{timestamp}] Response: {response}\n")
                f.write(f"[{timestamp}] Success: {success}\n\n")
        except:
            pass
    
    def analyze_task_complexity(self, query):
        """Analyze if task requires multiple steps"""
        complexity_keywords = [
            "multiple", "several", "steps", "first", "then", "after", "before",
            "complex", "complicated", "setup", "install", "configure", "build",
            "deploy", "migrate", "backup", "restore", "analyze", "process"
        ]
        
        query_lower = query.lower()
        complexity_score = sum(1 for keyword in complexity_keywords if keyword in query_lower)
        
        return complexity_score > 2
    
    def generate_response(self, query, context=None, mode="command"):
        """Generate AI response based on mode"""
        system_info = self.get_system_info()
        recent_commands = self.get_recent_commands()
        previous_context = self.load_context()
        
        # Build context-aware prompt
        prompt = f"""
You are an advanced terminal assistant for {system_info['os']} systems.

SYSTEM CONTEXT:
- OS: {system_info['os']} {system_info['os_version']}
- Shell: {system_info['shell']}
- Current directory: {system_info['current_dir']}
- User: {system_info['user']}

RECENT COMMANDS:
{chr(10).join(recent_commands[-5:])}

AVAILABLE COMMANDS (partial list):
{', '.join(system_info['available_commands'][:20])}

DIRECTORY STRUCTURE:
{system_info['directory_structure']}

PREVIOUS CONTEXT:
{json.dumps(previous_context, indent=2) if previous_context else 'None'}

USER REQUEST: {query}

"""

        if mode == "command":
            prompt += """
TASK: Generate a single, valid shell command that accomplishes the user's request.
- Return ONLY the command, no explanations
- Ensure it's compatible with the current OS and shell
- Use available commands when possible
- Consider recent command patterns
"""
        elif mode == "plan":
            prompt += """
TASK: Break down this complex task into a step-by-step plan.
- Return a JSON array of steps
- Each step should have: "description", "command", "explanation"
- Ensure commands are compatible with the current system
"""
        elif mode == "explain":
            prompt += """
TASK: Explain what the user is trying to accomplish and suggest the best approach.
- Provide a clear explanation
- Suggest alternative approaches if applicable
- Include any warnings or considerations
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful terminal assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=500 if mode == "command" else 1000
            )
            
            result = response.choices[0].message.content.strip()
            self.log_interaction(query, result, True)
            return result
            
        except AuthenticationError:
            print("❌ Invalid OpenAI API key. Please check OPENAI_API_KEY.")
            sys.exit(1)
        except Exception as e:
            print(f"❌ LLM error: {e}")
            sys.exit(1)
    
    def execute_multi_step_plan(self, plan_json):
        """Execute a multi-step plan"""
        try:
            steps = json.loads(plan_json)
            if not isinstance(steps, list):
                print("❌ Invalid plan format")
                return False
                
            print(f"\n📋 Executing {len(steps)} steps:")
            
            for i, step in enumerate(steps, 1):
                print(f"\n--- Step {i}: {step.get('description', 'Unknown')} ---")
                if 'explanation' in step:
                    print(f"💡 {step['explanation']}")
                
                command = step.get('command', '')
                if not command:
                    print("❌ No command specified for this step")
                    continue
                
                print(f"🤖 Command: {command}")
                response = input("🚀 Execute this step? [y/N/s] (s=skip): ").lower()
                
                if response == 's':
                    print("⏭️ Skipping step")
                    continue
                elif response == 'y':
                    try:
                        result = subprocess.run(command, shell=True, capture_output=True, text=True)
                        if result.stdout:
                            print(f"📤 Output: {result.stdout}")
                        if result.stderr:
                            print(f"⚠️ Errors: {result.stderr}")
                        if result.returncode != 0:
                            print(f"❌ Step failed with exit code {result.returncode}")
                            retry = input("🔄 Retry this step? [y/N]: ").lower()
                            if retry == 'y':
                                i -= 1  # Retry this step
                                continue
                    except Exception as e:
                        print(f"❌ Error executing command: {e}")
                else:
                    print("⏭️ Skipping step")
            
            return True
            
        except json.JSONDecodeError:
            print("❌ Invalid JSON in plan")
            return False
        except Exception as e:
            print(f"❌ Error executing plan: {e}")
            return False 