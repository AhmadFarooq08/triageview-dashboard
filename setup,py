#!/usr/bin/env python3
"""
TriageView Setup Script
Automates the initial setup and configuration for the TriageView dashboard.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def print_header():
    """Print setup header"""
    print("=" * 60)
    print("🏥 TriageView Dashboard Setup")
    print("AI-Powered Veteran Mental Health Triage System")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]}")

def check_git():
    """Check if git is available"""
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
        print("✅ Git is available")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  Git not found - manual repository setup required")
        return False

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        print("Please run: pip install -r requirements.txt")
        return False
    return True

def setup_api_key():
    """Configure Gemini API key"""
    print("\n🔑 API Key Configuration")
    print("Get your free Gemini API key from: https://makersuite.google.com/app/apikey")
    
    api_key = input("Enter your Gemini API key (or press Enter to skip): ").strip()
    
    if not api_key:
        print("⚠️  API key not provided - you'll need to configure it manually")
        return False
    
    # Create .streamlit directory if it doesn't exist
    streamlit_dir = Path(".streamlit")
    streamlit_dir.mkdir(exist_ok=True)
    
    # Create secrets.toml file
    secrets_file = streamlit_dir / "secrets.toml"
    with open(secrets_file, "w") as f:
        f.write(f'GEMINI_API_KEY = "{api_key}"\n')
    
    print("✅ API key configured in .streamlit/secrets.toml")
    return True

def test_installation():
    """Test if the application can start"""
    print("\n🧪 Testing installation...")
    try:
        # Test import of main modules
        import streamlit
        import pandas
        import plotly
        import requests
        print("✅ All required modules imported successfully")
        
        # Test API key access
        if os.path.exists(".streamlit/secrets.toml"):
            print("✅ API key configuration found")
        else:
            print("⚠️  API key not configured - some features may not work")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def create_launch_script():
    """Create a launch script for easy startup"""
    print("\n📝 Creating launch script...")
    
    # Windows batch file
    with open("launch.bat", "w") as f:
        f.write("@echo off\n")
        f.write("echo Starting TriageView Dashboard...\n")
        f.write("streamlit run triage_dashboard_2.py\n")
        f.write("pause\n")
    
    # Unix shell script
    with open("launch.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("echo 'Starting TriageView Dashboard...'\n")
        f.write("streamlit run triage_dashboard_2.py\n")
    
    # Make shell script executable
    try:
        os.chmod("launch.sh", 0o755)
    except:
        pass
    
    print("✅ Launch scripts created (launch.bat for Windows, launch.sh for Unix)")

def setup_git_repository():
    """Initialize git repository if not already done"""
    print("\n📁 Git Repository Setup")
    
    if not os.path.exists(".git"):
        try:
            subprocess.run(["git", "init"], check=True, capture_output=True)
            subprocess.run(["git", "add", "."], check=True, capture_output=True)
            subprocess.run(["git", "commit", "-m", "Initial commit"], check=True, capture_output=True)
            print("✅ Git repository initialized")
        except subprocess.CalledProcessError:
            print("⚠️  Git repository setup failed")
    else:
        print("✅ Git repository already exists")

def print_next_steps():
    """Print next steps for the user"""
    print("\n" + "=" * 60)
    print("🎉 Setup Complete!")
    print("=" * 60)
    print()
    print("Next Steps:")
    print("1. 🚀 Start the application:")
    print("   • Windows: double-click launch.bat")
    print("   • Unix/Mac: ./launch.sh")
    print("   • Manual: streamlit run triage_dashboard_2.py")
    print()
    print("2. 🌐 Open your browser to: http://localhost:8501")
    print()
    print("3. 📚 Read the documentation:")
    print("   • README.md - Complete project overview")
    print("   • DEPLOYMENT.md - Deployment instructions")
    print()
    print("4. 🚀 Deploy to Streamlit Cloud:")
    print("   • Push to GitHub repository")
    print("   • Visit https://share.streamlit.io/")
    print("   • Connect your repository")
    print()
    print("5. 🔧 Configuration files created:")
    print("   • .streamlit/config.toml - Streamlit settings")
    print("   • .streamlit/secrets.toml - API key (if provided)")
    print("   • requirements.txt - Dependencies")
    print()
    print("For support, visit: https://github.com/yourusername/triageview-dashboard")
    print("=" * 60)

def main():
    """Main setup function"""
    print_header()
    
    # Check prerequisites
    check_python_version()
    git_available = check_git()
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Setup failed - please resolve dependency issues")
        sys.exit(1)
    
    # Configure API key
    setup_api_key()
    
    # Test installation
    if not test_installation():
        print("❌ Installation test failed")
        sys.exit(1)
    
    # Create helper scripts
    create_launch_script()
    
    # Setup git if available
    if git_available:
        setup_git_repository()
    
    # Print completion message
    print_next_steps()

if __name__ == "__main__":
    main()
