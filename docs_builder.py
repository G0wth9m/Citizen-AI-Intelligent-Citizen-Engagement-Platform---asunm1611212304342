#!/usr/bin/env python3
"""
CitizenAI Documentation Builder and Deployer

This script helps build and deploy the CitizenAI documentation.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"📋 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Error: {e.stderr}")
        sys.exit(1)

def check_requirements():
    """Check if required tools are available."""
    print("🔍 Checking requirements...")
    
    # Check Python
    try:
        import mkdocs
        print("✅ MkDocs is installed")
    except ImportError:
        print("❌ MkDocs not found. Installing...")
        run_command("pip install mkdocs mkdocs-material mkdocs-mermaid2-plugin", "Installing MkDocs")
    
    # Check if in correct directory
    if not os.path.exists('mkdocs.yml'):
        print("❌ mkdocs.yml not found. Are you in the project root directory?")
        sys.exit(1)
    
    print("✅ All requirements met")

def build_docs():
    """Build the documentation."""
    run_command("mkdocs build", "Building documentation")

def serve_docs():
    """Serve documentation locally."""
    print("🌐 Starting local development server...")
    print("📖 Documentation will be available at: http://127.0.0.1:8000/Citizen-AI/")
    print("🔄 Press Ctrl+C to stop the server")
    
    try:
        subprocess.run(["mkdocs", "serve"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Documentation server stopped")

def deploy_github():
    """Deploy to GitHub Pages."""
    print("🚀 Deploying to GitHub Pages...")
    
    # Check if git repo
    if not os.path.exists('.git'):
        print("❌ Not a git repository. Initialize git first:")
        print("   git init")
        print("   git remote add origin https://github.com/AkhileshMalthi/Citizen-AI.git")
        sys.exit(1)
    
    # Deploy using mkdocs
    run_command("mkdocs gh-deploy", "Deploying to GitHub Pages")
    print("🎉 Documentation deployed successfully!")
    print("🌐 Available at: https://akhileshmalthi.github.io/Citizen-AI/")

def clean_build():
    """Clean build artifacts."""
    run_command("mkdocs build --clean", "Cleaning and rebuilding documentation")

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="CitizenAI Documentation Builder")
    parser.add_argument("command", choices=['build', 'serve', 'deploy', 'clean'], 
                       help="Command to execute")
    
    args = parser.parse_args()
    
    print("📚 CitizenAI Documentation Builder")
    print("=" * 40)
    
    check_requirements()
    
    if args.command == 'build':
        build_docs()
        print("\n🎉 Documentation built successfully!")
        print("📁 Output directory: site/")
        
    elif args.command == 'serve':
        serve_docs()
        
    elif args.command == 'deploy':
        build_docs()
        deploy_github()
        
    elif args.command == 'clean':
        clean_build()
        print("\n🎉 Documentation cleaned and rebuilt!")

if __name__ == "__main__":
    main()
