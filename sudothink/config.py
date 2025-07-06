#!/usr/bin/env python3
"""
Configuration management for SudoThink
"""

import os
import json
import getpass
from pathlib import Path

class Config:
    def __init__(self):
        self.config_dir = Path.home() / ".sudothink"
        self.config_file = self.config_dir / "config.json"
        self._ensure_config_dir()
    
    def _ensure_config_dir(self):
        """Ensure configuration directory exists with proper permissions"""
        if not self.config_dir.exists():
            self.config_dir.mkdir(mode=0o700)  # Only owner can read/write/execute
    
    def get_api_key(self):
        """Get API key from environment or config file"""
        # First try environment variable
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            return api_key
        
        # Then try config file
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    return config.get("openai_api_key")
            except (json.JSONDecodeError, IOError):
                pass
        
        return None
    
    def set_api_key(self, api_key=None):
        """Set API key in config file"""
        if api_key is None:
            api_key = getpass.getpass("Enter your OpenAI API key: ")
        
        if not api_key.strip():
            raise ValueError("API key cannot be empty")
        
        # Validate API key format (basic check)
        if not api_key.startswith("sk-"):
            raise ValueError("Invalid API key format. OpenAI API keys start with 'sk-'")
        
        config = {}
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        
        config["openai_api_key"] = api_key
        
        # Write config with restricted permissions
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        # Set file permissions to owner only
        os.chmod(self.config_file, 0o600)
        
        return True
    
    def remove_api_key(self):
        """Remove API key from config file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                
                if "openai_api_key" in config:
                    del config["openai_api_key"]
                    
                    with open(self.config_file, 'w') as f:
                        json.dump(config, f, indent=2)
                    
                    return True
            except (json.JSONDecodeError, IOError):
                pass
        
        return False
    
    def has_api_key(self):
        """Check if API key is configured"""
        return self.get_api_key() is not None 