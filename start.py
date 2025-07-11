#!/usr/bin/env python3
"""
Startup script for Byte-Sized Brilliance Newsletter Website
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]}")

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        sys.exit(1)

def create_sample_pdf():
    """Create a sample PDF if it doesn't exist"""
    sample_pdf = Path("newsletters/sample-newsletter.pdf")
    if not sample_pdf.exists():
        print("📄 Creating sample PDF...")
        try:
            from create_sample_pdf import create_sample_pdf
            create_sample_pdf()
            print("✅ Sample PDF created")
        except ImportError:
            print("⚠️  Could not create sample PDF (reportlab not available)")

def setup_environment():
    """Set up the environment"""
    print("🚀 Setting up Byte-Sized Brilliance Newsletter Website")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Create necessary directories
    os.makedirs("newsletters", exist_ok=True)
    os.makedirs("templates", exist_ok=True)
    
    # Install dependencies
    install_dependencies()
    
    # Create sample PDF
    create_sample_pdf()
    
    print("✅ Environment setup complete!")

def start_server():
    """Start the Flask server"""
    print("\n🌐 Starting server...")
    print("📍 Website will be available at: http://localhost:5000")
    print("🔐 Admin panel: http://localhost:5000/admin")
    print("👤 Admin credentials: admin / admin123")
    print("\n" + "=" * 50)
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Open browser after a short delay
    def open_browser():
        time.sleep(2)
        try:
            webbrowser.open("http://localhost:5000")
        except:
            pass
    
    import threading
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Start Flask app
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

def main():
    """Main function"""
    if len(sys.argv) > 1 and sys.argv[1] == "--setup":
        setup_environment()
        return
    
    # Check if setup is needed
    if not Path("templates").exists() or not Path("app.py").exists():
        print("⚠️  Setup required. Running setup...")
        setup_environment()
    
    start_server()

if __name__ == "__main__":
    main() 