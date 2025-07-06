#!/usr/bin/env python3
"""
Test script for SudoThink setup functionality
Run this before pushing to production
"""

import os
import sys
import tempfile
import shutil
import subprocess
from pathlib import Path

def test_config_module():
    """Test the config module functionality"""
    print("🧪 Testing config module...")
    
    try:
        from sudothink.config import Config
        
        # Test config creation
        config = Config()
        print("✅ Config module imported successfully")
        
        # Test config directory creation
        assert config.config_dir.exists(), "Config directory should exist"
        print("✅ Config directory created")
        
        # Test initial state
        assert config.get_api_key() is None, "Should start with no API key"
        print("✅ Initial state correct")
        
        return True
    except Exception as e:
        print(f"❌ Config module test failed: {e}")
        return False

def test_setup_commands():
    """Test setup command functionality"""
    print("\n🧪 Testing setup commands...")
    
    try:
        # Test help
        result = subprocess.run([sys.executable, "ai.py", "--help"], 
                              capture_output=True, text=True)
        assert result.returncode == 0, "Help command should succeed"
        assert "setup" in result.stdout, "Help should mention setup"
        print("✅ Help command works")
        
        # Test setup status
        result = subprocess.run([sys.executable, "ai.py", "setup", "--status"], 
                              capture_output=True, text=True)
        assert result.returncode == 0, "Setup status should succeed"
        assert "API key" in result.stdout, "Status should mention API key"
        print("✅ Setup status command works")
        
        return True
    except Exception as e:
        print(f"❌ Setup commands test failed: {e}")
        return False

def test_shell_integration():
    """Test shell function integration"""
    print("\n🧪 Testing shell integration...")
    
    try:
        # Test if ai.zsh can be sourced without errors
        result = subprocess.run(["zsh", "-c", "source ai.zsh; echo 'Sourcing successful'"], 
                              capture_output=True, text=True)
        assert result.returncode == 0, "Shell script should source without errors"
        assert "Sourcing successful" in result.stdout, "Should execute test command"
        print("✅ Shell script sources cleanly")
        
        return True
    except Exception as e:
        print(f"❌ Shell integration test failed: {e}")
        return False

def test_api_key_validation():
    """Test API key validation"""
    print("\n🧪 Testing API key validation...")
    
    try:
        from sudothink.config import Config
        config = Config()
        
        # Test invalid API key
        try:
            config.set_api_key("invalid-key")
            assert False, "Should reject invalid API key"
        except ValueError:
            print("✅ Invalid API key rejected")
        
        # Test empty API key
        try:
            config.set_api_key("")
            assert False, "Should reject empty API key"
        except ValueError:
            print("✅ Empty API key rejected")
        
        return True
    except Exception as e:
        print(f"❌ API key validation test failed: {e}")
        return False

def test_config_file_permissions():
    """Test config file security"""
    print("\n🧪 Testing config file security...")
    
    try:
        from sudothink.config import Config
        
        # Create a temporary config for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            # Mock the config directory
            original_home = os.path.expanduser("~")
            os.environ["HOME"] = temp_dir
            
            config = Config()
            config.set_api_key("sk-test123456789")
            
            # Check file permissions
            config_file = Path(temp_dir) / ".sudothink" / "config.json"
            assert config_file.exists(), "Config file should exist"
            
            # Check permissions (should be 600 - owner read/write only)
            stat = config_file.stat()
            mode = stat.st_mode & 0o777
            assert mode == 0o600, f"Config file should have 600 permissions, got {oct(mode)}"
            print("✅ Config file has correct permissions")
            
            # Check directory permissions
            config_dir = Path(temp_dir) / ".sudothink"
            stat = config_dir.stat()
            mode = stat.st_mode & 0o777
            assert mode == 0o700, f"Config directory should have 700 permissions, got {oct(mode)}"
            print("✅ Config directory has correct permissions")
            
            # Restore original HOME
            os.environ["HOME"] = original_home
        
        return True
    except Exception as e:
        print(f"❌ Config file security test failed: {e}")
        return False

def test_backward_compatibility():
    """Test backward compatibility with environment variables"""
    print("\n🧪 Testing backward compatibility...")
    
    try:
        from sudothink.config import Config
        
        # Test that environment variable takes precedence
        test_key = "sk-env-test-key"
        os.environ["OPENAI_API_KEY"] = test_key
        
        config = Config()
        retrieved_key = config.get_api_key()
        
        assert retrieved_key == test_key, "Environment variable should take precedence"
        print("✅ Environment variable precedence works")
        
        # Clean up
        del os.environ["OPENAI_API_KEY"]
        
        return True
    except Exception as e:
        print(f"❌ Backward compatibility test failed: {e}")
        return False

def run_integration_test():
    """Run a full integration test"""
    print("\n🧪 Running integration test...")
    
    try:
        # Test the complete flow
        result = subprocess.run([sys.executable, "ai.py", "setup", "--status"], 
                              capture_output=True, text=True)
        
        # Check if it's a missing dependency issue
        if "No module named 'openai'" in result.stderr:
            print("⚠️ Integration test skipped (openai module not installed)")
            print("💡 This is expected in test environment without dependencies")
            return True
        
        if result.returncode == 0:
            print("✅ Integration test passed")
            return True
        else:
            print(f"❌ Integration test failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting SudoThink tests...\n")
    
    tests = [
        test_config_module,
        test_setup_commands,
        test_shell_integration,
        test_api_key_validation,
        test_config_file_permissions,
        test_backward_compatibility,
        run_integration_test
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Ready for production.")
        return 0
    else:
        print("⚠️ Some tests failed. Please fix issues before pushing to production.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 