# Pre-Commit Checklist for SudoThink

## 🧪 Automated Tests

### 1. Run Test Suite
```bash
python3 test_setup.py
```
**Expected**: All tests should pass (7/7)

### 2. Manual Testing Checklist

#### Setup Commands
- [ ] `ai setup --status` shows correct status
- [ ] `ai setup --help` shows help
- [ ] `ai setup --remove` removes config (if exists)
- [ ] `ai setup` prompts for API key interactively
- [ ] `ai setup --api-key "sk-test"` works non-interactively

#### Shell Integration
- [ ] `source ai.zsh` produces no output
- [ ] `ai --help` works
- [ ] `ai setup --status` works from shell
- [ ] `ai-setup --status` works (helper function)

#### API Key Management
- [ ] Invalid API keys are rejected
- [ ] Empty API keys are rejected
- [ ] Valid API keys are accepted
- [ ] Config file has correct permissions (600)
- [ ] Config directory has correct permissions (700)

#### Backward Compatibility
- [ ] `OPENAI_API_KEY` environment variable takes precedence
- [ ] Old workflow still works with env var
- [ ] New workflow works without env var

## 🔍 Code Quality Checks

### 3. Syntax Check
```bash
python3 -m py_compile sudothink/config.py
python3 -m py_compile sudothink/setup.py
python3 -m py_compile sudothink/assistant.py
python3 -m py_compile sudothink/cli.py
python3 -m py_compile ai.py
```

### 4. Import Check
```bash
python3 -c "from sudothink.config import Config; print('Config OK')"
python3 -c "from sudothink.setup import main; print('Setup OK')"
python3 -c "from sudothink.assistant import AITerminalAssistant; print('Assistant OK')"
```

### 5. Shell Script Validation
```bash
zsh -n ai.zsh  # Check syntax without executing
```

## 📚 Documentation

### 6. Documentation Review
- [ ] README.md updated with setup instructions
- [ ] All new commands documented
- [ ] Examples are clear and accurate
- [ ] Troubleshooting section updated

### 7. Help Text Verification
```bash
python3 ai.py --help
python3 ai.py setup --help
```
- [ ] Help text is clear and complete
- [ ] All options documented
- [ ] Examples provided where helpful

## 🔒 Security Review

### 8. Security Checks
- [ ] API keys are not logged or printed
- [ ] Config file permissions are restrictive (600)
- [ ] Config directory permissions are restrictive (700)
- [ ] No sensitive data in error messages
- [ ] Input validation prevents injection

### 9. File Permissions
```bash
ls -la ~/.sudothink/config.json  # Should be 600
ls -ld ~/.sudothink/             # Should be 700
```

## 🚀 Production Readiness

### 10. Installation Test
```bash
# Test fresh installation
cd /tmp
git clone <your-repo> test-sudothink
cd test-sudothink
python3 ai.py setup --status  # Should work without existing config
```

### 11. Error Handling
- [ ] Graceful handling of missing config
- [ ] Clear error messages for users
- [ ] No crashes on invalid input
- [ ] Proper exit codes

### 12. Performance
- [ ] No significant delay when sourcing ai.zsh
- [ ] Setup commands respond quickly
- [ ] No memory leaks in repeated usage

## 📋 Final Checklist

### Before Pushing
- [ ] All automated tests pass
- [ ] Manual testing completed
- [ ] Documentation updated
- [ ] Security review passed
- [ ] Code reviewed (if applicable)
- [ ] Version numbers updated (if needed)
- [ ] Changelog updated (if applicable)

### Post-Push Verification
- [ ] Test installation from fresh environment
- [ ] Verify setup works for new users
- [ ] Check that existing users aren't broken
- [ ] Monitor for any immediate issues

## 🆘 If Tests Fail

### Common Issues and Fixes

1. **Import Errors**
   - Check file paths and imports
   - Verify `__init__.py` files exist
   - Test with absolute imports

2. **Permission Errors**
   - Ensure proper file permissions
   - Check directory creation logic
   - Verify umask settings

3. **Shell Integration Issues**
   - Check for syntax errors in ai.zsh
   - Verify function definitions
   - Test sourcing in clean environment

4. **API Key Issues**
   - Verify validation logic
   - Check config file format
   - Test environment variable precedence

## 🎯 Success Criteria

**Ready for production when:**
- ✅ All automated tests pass
- ✅ Manual testing checklist complete
- ✅ No security issues identified
- ✅ Documentation is current
- ✅ Error handling is robust
- ✅ Backward compatibility maintained 