# Installation

This guide will help you install and set up CitizenAI on your system.

## Prerequisites

Before installing CitizenAI, ensure you have the following prerequisites:

!!! info "System Requirements"
    - **Python**: 3.11 or higher
    - **Operating System**: Windows, macOS, or Linux
    - **Memory**: At least 4GB RAM recommended
    - **Storage**: 1GB free disk space

### Required Software

=== "Python"
    ```bash
    # Check Python version
    python --version
    # Should return Python 3.11.x or higher
    ```

=== "Git"
    ```bash
    # Install Git (if not already installed)
    # Windows: Download from https://git-scm.com/
    # macOS: brew install git
    # Linux: sudo apt-get install git
    
    # Verify installation
    git --version
    ```

=== "pip"
    ```bash
    # pip is included with Python 3.11+
    # Verify installation
    pip --version
    ```

## Installation Methods

### Method 1: Clone from GitHub (Recommended)

```bash
# Clone the repository
git clone https://github.com/AkhileshMalthi/Citizen-AI.git

# Navigate to the project directory
cd Citizen-AI

# Create a virtual environment (recommended)
python -m venv .venv

# Activate the virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Method 2: Download ZIP

1. Go to the [GitHub repository](https://github.com/AkhileshMalthi/Citizen-AI)
2. Click on "Code" → "Download ZIP"
3. Extract the ZIP file to your desired location
4. Open terminal/command prompt in the extracted folder
5. Follow steps 3-6 from Method 1

## Dependencies

CitizenAI relies on several Python packages:

```txt title="requirements.txt"
Flask==2.3.3
flask-session==0.5.0
requests==2.31.0
python-dotenv==1.0.0
ibm-watson==7.0.1
ibm-cloud-sdk-core==3.18.0
plotly==5.17.0
pandas==2.1.3
numpy==1.25.2
Werkzeug==2.3.7
```

!!! tip "Virtual Environment"
    It's highly recommended to use a virtual environment to avoid conflicts with other Python projects:
    
    ```bash
    # Create virtual environment
    python -m venv citizenai-env
    
    # Activate it
    # Windows:
    citizenai-env\Scripts\activate
    # macOS/Linux:
    source citizenai-env/bin/activate
    ```

## Verification

After installation, verify that everything is working correctly:

```bash
# Run the demo version (lightweight, no AI dependencies)
python app_demo.py

# You should see output similar to:
# * Running on http://127.0.0.1:5000
# * Debug mode: on
```

Open your web browser and navigate to `http://localhost:5000`. You should see the CitizenAI interface.

## Troubleshooting

### Common Issues

??? question "Python version issues"
    If you're getting Python version errors:
    
    ```bash
    # Check your Python version
    python --version
    
    # If using Python 3.11+ but still getting errors, try:
    python3 --version
    python3.11 --version
    ```

??? question "Permission errors during installation"
    On Windows, try running as administrator:
    ```bash
    # Run command prompt as administrator
    pip install -r requirements.txt
    ```
    
    On macOS/Linux:
    ```bash
    sudo pip install -r requirements.txt
    # Or better, use a virtual environment
    ```

??? question "Module not found errors"
    Ensure you're in the correct directory and virtual environment:
    ```bash
    # Check current directory
    pwd  # or cd on Windows
    
    # Ensure virtual environment is activated
    which python  # or where python on Windows
    ```

### Getting Help

If you encounter issues not covered here:

1. Check the [Troubleshooting](../support/troubleshooting.md) section
2. Search existing [GitHub Issues](https://github.com/AkhileshMalthi/Citizen-AI/issues)
3. Create a new issue with detailed error information

## Next Steps

Once installation is complete, proceed to the [Quick Start](quick-start.md) guide to learn how to configure and run CitizenAI.
