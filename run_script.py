#!/usr/bin/env python3
"""
RIA - Regulatory Impact Analyzer
Quick run script for development and testing
"""

import subprocess
import sys
import os

def check_requirements():
    """Check if all required packages are installed"""
    required_packages = [
        'streamlit',
        'pandas', 
        'plotly',
        'numpy'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n🔧 Please install requirements using:")
        print("   pip install -r requirements.txt")
        return False
    
    print("✅ All required packages are installed!")
    return True

def run_app():
    """Run the Streamlit application"""
    if not check_requirements():
        sys.exit(1)
    
    print("🚀 Starting RIA - Regulatory Impact Analyzer...")
    print("📱 Application will open in your default browser")
    print("🔗 URL: http://localhost:8501")
    print("\n⚡ Press Ctrl+C to stop the application\n")
    
    # Run streamlit app
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "ria_main_app.py",
            "--server.port", "8501",
            "--server.headless", "false",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n\n👋 Application stopped. Thank you for using RIA!")
    except Exception as e:
        print(f"❌ Error running application: {e}")

if __name__ == "__main__":
    run_app()
