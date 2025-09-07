# Troubleshooting

This guide helps you diagnose and resolve common issues with CitizenAI.

## Quick Diagnostics

### Health Check Script

Create a simple health check to verify your setup:

```python title="health_check.py"
#!/usr/bin/env python3

import sys
import subprocess
import os
from pathlib import Path

def check_python_version():
    """Check Python version."""
    version = sys.version_info
    if version.major == 3 and version.minor >= 11:
        print("✅ Python version OK:", sys.version)
        return True
    else:
        print("❌ Python version too old:", sys.version)
        print("   Required: Python 3.11+")
        return False

def check_dependencies():
    """Check if required packages are installed."""
    required_packages = [
        'flask', 'requests', 'python-dotenv', 
        'plotly', 'pandas', 'numpy'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} installed")
        except ImportError:
            print(f"❌ {package} missing")
            missing.append(package)
    
    return len(missing) == 0

def check_environment():
    """Check environment configuration."""
    required_files = ['.env', 'app.py', 'app_demo.py']
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} found")
        else:
            print(f"❌ {file} missing")

def check_ports():
    """Check if required ports are available."""
    import socket
    
    def is_port_open(port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        return result == 0
    
    if is_port_open(5000):
        print("⚠️  Port 5000 is in use")
        return False
    else:
        print("✅ Port 5000 available")
        return True

if __name__ == "__main__":
    print("CitizenAI Health Check")
    print("=" * 30)
    
    checks = [
        check_python_version(),
        check_dependencies(),
        check_ports()
    ]
    
    check_environment()
    
    if all(checks):
        print("\n🎉 All checks passed! CitizenAI should work correctly.")
    else:
        print("\n🔧 Some issues found. Please resolve them before running CitizenAI.")
```

Run this script to diagnose common issues:

```bash
python health_check.py
```

## Common Issues

### Installation Problems

#### Issue: pip install fails with permission errors

**Symptoms:**
```
ERROR: Could not install packages due to an EnvironmentError: 
[Errno 13] Permission denied
```

**Solution:**
```bash
# Use virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
pip install -r requirements.txt

# OR use user installation
pip install --user -r requirements.txt
```

#### Issue: Python version not supported

**Symptoms:**
```
ERROR: Package requires a different Python version
```

**Solution:**
1. **Check Python version**:
   ```bash
   python --version
   ```

2. **Install Python 3.11+**:
   - **Windows**: Download from [python.org](https://python.org)
   - **macOS**: `brew install python@3.11`
   - **Linux**: `sudo apt install python3.11`

3. **Use specific Python version**:
   ```bash
   python3.11 -m venv .venv
   ```

#### Issue: Virtual environment activation fails

**Windows PowerShell:**
```powershell
# Enable execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate
.venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
# Check shell type
echo $SHELL

# For bash
source .venv/bin/activate

# For fish
source .venv/bin/activate.fish

# For csh
source .venv/bin/activate.csh
```

### Application Startup Issues

#### Issue: "ModuleNotFoundError" when running app

**Symptoms:**
```
ModuleNotFoundError: No module named 'flask'
```

**Diagnosis:**
```bash
# Check if virtual environment is activated
which python  # Should show venv path

# Check installed packages
pip list | grep flask
```

**Solution:**
```bash
# Ensure virtual environment is activated
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### Issue: Port 5000 already in use

**Symptoms:**
```
OSError: [Errno 48] Address already in use
```

**Find what's using the port:**
```bash
# macOS/Linux
lsof -i :5000

# Windows
netstat -ano | findstr :5000
```

**Solutions:**
1. **Kill existing process:**
   ```bash
   # macOS/Linux
   kill -9 <PID>
   
   # Windows
   taskkill /PID <PID> /F
   ```

2. **Use different port:**
   ```python
   # In app.py or app_demo.py
   app.run(host='0.0.0.0', port=5001, debug=True)
   ```

3. **Set port via environment:**
   ```bash
   export PORT=5001
   python app_demo.py
   ```

#### Issue: Application starts but pages don't load

**Check browser console** for JavaScript errors:
1. Open developer tools (F12)
2. Check Console tab for errors
3. Check Network tab for failed requests

**Common fixes:**
```bash
# Clear browser cache
# Hard refresh: Ctrl+F5 (Windows) or Cmd+Shift+R (macOS)

# Check if static files are loading
curl http://localhost:5000/static/css/styles.css
```

### Watson AI Integration Issues

#### Issue: Watson API authentication fails

**Symptoms:**
```
Unauthorized: Invalid API key
```

**Check credentials:**
```bash
# Verify .env file exists and has correct format
cat .env | grep WATSON

# Test API key manually
curl -u "apikey:YOUR_API_KEY" \
  "https://api.us-south.assistant.watson.cloud.ibm.com/instances/YOUR_INSTANCE_ID/v2/assistants?version=2021-06-14"
```

**Solution:**
1. **Verify Watson credentials** in IBM Cloud console
2. **Check .env file format**:
   ```bash
   WATSON_API_KEY=your-actual-api-key-here
   WATSON_URL=https://api.us-south.assistant.watson.cloud.ibm.com/instances/your-instance-id
   ```
3. **Restart application** after changing .env

#### Issue: Watson responses are slow or timeout

**Check network connectivity:**
```bash
# Test Watson endpoint
curl -I https://api.us-south.assistant.watson.cloud.ibm.com

# Check DNS resolution
nslookup api.us-south.assistant.watson.cloud.ibm.com
```

**Solutions:**
1. **Increase timeout values**:
   ```python
   # In Watson configuration
   timeout = 30  # seconds
   ```

2. **Check firewall/proxy settings**
3. **Use demo version** if Watson is unavailable:
   ```bash
   python app_demo.py
   ```

### Performance Issues

#### Issue: Application is slow or unresponsive

**Check system resources:**
```bash
# Check memory usage
free -h  # Linux
vm_stat  # macOS

# Check CPU usage
top      # Linux/macOS
```

**Check application logs:**
```bash
# Enable debug logging
export FLASK_DEBUG=1
python app_demo.py

# Check for errors in output
```

**Solutions:**
1. **Increase available memory**
2. **Use production WSGI server**:
   ```bash
   pip install gunicorn
   gunicorn -w 4 app:app
   ```
3. **Enable caching**
4. **Optimize database queries**

#### Issue: High memory usage

**Monitor memory usage:**
```python
import psutil
import os

def get_memory_usage():
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    return memory_info.rss / 1024 / 1024  # MB

print(f"Memory usage: {get_memory_usage():.2f} MB")
```

**Solutions:**
1. **Use pagination** for large datasets
2. **Implement data streaming**
3. **Clear unused variables**
4. **Optimize data structures**

### Database and Storage Issues

#### Issue: Session data not persisting

**Check session directory:**
```bash
# Look for flask_session directory
ls -la flask_session/

# Check permissions
ls -la flask_session/
```

**Solution:**
```python
# Ensure session directory is writable
import os
os.makedirs('flask_session', exist_ok=True)

# Check Flask session configuration
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './flask_session'
```

#### Issue: Analytics data not saving

**Check data directory permissions:**
```bash
# Check if data directory exists and is writable
ls -la data/
chmod 755 data/  # Fix permissions if needed
```

**Verify file operations:**
```python
import json
import os

# Test file write
test_data = {"test": "data"}
try:
    with open('data/test.json', 'w') as f:
        json.dump(test_data, f)
    print("File write successful")
    os.remove('data/test.json')  # Cleanup
except Exception as e:
    print(f"File write failed: {e}")
```

### Browser and Frontend Issues

#### Issue: JavaScript errors in browser console

**Common JavaScript errors:**

1. **"Cannot read property of undefined"**
   - Check if required data is loaded
   - Verify API endpoints are responding

2. **"Chart is not defined"**
   - Ensure Plotly.js is loaded
   - Check network requests in browser dev tools

3. **"CSRF token missing"**
   - Check if CSRF protection is properly configured
   - Verify forms include CSRF tokens

**Debug steps:**
```javascript
// Open browser console and test
console.log("Testing JavaScript");

// Check if libraries are loaded
console.log(typeof Plotly);  // Should not be "undefined"
console.log(typeof $);       // Should not be "undefined" if using jQuery
```

#### Issue: Styles not loading correctly

**Check CSS loading:**
```bash
# Test if CSS file is accessible
curl http://localhost:5000/static/css/styles.css
```

**Check browser cache:**
1. Open Developer Tools (F12)
2. Right-click refresh button
3. Select "Empty Cache and Hard Reload"

**Verify file paths:**
```html
<!-- Check if paths are correct in templates -->
<link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
```

## Debugging Techniques

### Enable Debug Mode

```python
# Method 1: Environment variable
export FLASK_DEBUG=1
python app_demo.py

# Method 2: In code
app.run(debug=True)

# Method 3: Configuration
app.config['DEBUG'] = True
```

### Add Logging

```python
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Add debug statements
logger.debug("Processing chat message: %s", message)
logger.info("User authenticated: %s", username)
logger.warning("Watson API key not configured")
logger.error("Database connection failed: %s", error)
```

### Use Python Debugger

```python
import pdb

def problematic_function():
    # Set breakpoint
    pdb.set_trace()
    
    # Code execution will pause here
    # Use debugger commands:
    # n - next line
    # s - step into
    # c - continue
    # l - list code
    # p variable_name - print variable
```

### Network Debugging

```bash
# Check if service is responding
curl -v http://localhost:5000/

# Test specific endpoints
curl -X POST http://localhost:5000/api/v1/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "test"}'

# Check headers
curl -I http://localhost:5000/
```

## Getting Help

### Before Asking for Help

1. **Check this troubleshooting guide**
2. **Search existing GitHub issues**
3. **Enable debug mode** and check logs
4. **Run the health check script**
5. **Try the demo version** to isolate issues

### When Reporting Issues

Include this information:

```markdown
**Environment:**
- OS: Windows 10 / macOS 12.0 / Ubuntu 20.04
- Python version: 3.11.0
- Browser: Chrome 96.0.4664.110
- CitizenAI version: main branch / v1.0.0

**Issue Description:**
Clear description of the problem

**Steps to Reproduce:**
1. Step one
2. Step two
3. Expected vs actual result

**Error Messages:**
```
Paste complete error messages here
```

**Additional Context:**
- Configuration details
- Recent changes
- Workarounds attempted
```

### Emergency Troubleshooting

If nothing works, try this emergency reset:

```bash
# 1. Start fresh
rm -rf .venv/
rm -rf __pycache__/
rm -rf flask_session/

# 2. Recreate environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# 3. Reinstall everything
pip install --upgrade pip
pip install -r requirements.txt

# 4. Use minimal configuration
cp .env.example .env

# 5. Test with demo
python app_demo.py
```

---

!!! tip "Still Need Help?"
    If you're still experiencing issues:
    
    1. 🔍 Search [GitHub Issues](https://github.com/AkhileshMalthi/Citizen-AI/issues)
    2. 💬 Start a [GitHub Discussion](https://github.com/AkhileshMalthi/Citizen-AI/discussions)  
    3. 📝 Create a [new issue](https://github.com/AkhileshMalthi/Citizen-AI/issues/new) with detailed information
