#!/usr/bin/env python3
"""
Setup command for SudoThink
"""

import sys
import argparse
from .config import Config

def main():
    """Main setup function"""
    parser = argparse.ArgumentParser(description="Configure SudoThink")
    parser.add_argument("--api-key", help="OpenAI API key (will prompt if not provided)")
    parser.add_argument("--remove", action="store_true", help="Remove stored API key")
    parser.add_argument("--status", action="store_true", help="Show configuration status")
    
    args = parser.parse_args()
    
    config = Config()
    
    if args.status:
        if config.has_api_key():
            print("✅ API key is configured")
            api_key = config.get_api_key()
            if api_key:
                # Show first few characters for verification
                masked_key = api_key[:7] + "..." + api_key[-4:] if len(api_key) > 11 else "***"
                print(f"🔑 API Key: {masked_key}")
        else:
            print("❌ API key is not configured")
            print("💡 Run 'ai-setup' to configure your API key")
        return
    
    if args.remove:
        if config.remove_api_key():
            print("✅ API key removed from configuration")
        else:
            print("ℹ️ No API key was stored in configuration")
        return
    
    # Default action: configure API key
    try:
        if config.set_api_key(args.api_key):
            print("✅ API key configured successfully!")
            print("💡 You can now use the 'ai' command without setting OPENAI_API_KEY each time")
            print("🔒 Your API key is stored securely in ~/.sudothink/config.json")
    except ValueError as e:
        print(f"❌ Configuration failed: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n❌ Configuration cancelled")
        sys.exit(1)

if __name__ == "__main__":
    main() 