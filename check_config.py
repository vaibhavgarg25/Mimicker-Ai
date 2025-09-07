#!/usr/bin/env python3
"""
Configuration checker for Mimicker AI
Verifies all required environment variables and dependencies
"""

import os
import sys
from pathlib import Path

def check_file_exists(file_path, description):
    """Check if a file exists"""
    if os.path.exists(file_path):
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} (NOT FOUND)")
        return False

def check_env_file(env_path, required_vars):
    """Check environment file and required variables"""
    if not os.path.exists(env_path):
        print(f"❌ Environment file missing: {env_path}")
        return False
    
    print(f"✅ Environment file found: {env_path}")
    
    # Read and check variables
    with open(env_path, 'r') as f:
        content = f.read()
    
    missing_vars = []
    for var in required_vars:
        if f"{var}=" not in content:
            missing_vars.append(var)
    
    if missing_vars:
        print(f"   ⚠️  Missing variables: {', '.join(missing_vars)}")
        return False
    else:
        print(f"   ✅ All required variables present")
        return True

def check_python_packages(requirements_file):
    """Check if Python packages are installed"""
    if not os.path.exists(requirements_file):
        print(f"❌ Requirements file missing: {requirements_file}")
        return False
    
    print(f"📦 Checking Python packages from {requirements_file}...")
    
    with open(requirements_file, 'r') as f:
        packages = [line.strip().split('==')[0] for line in f if line.strip() and not line.startswith('#')]
    
    missing_packages = []
    for package in packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"   ❌ Missing packages: {', '.join(missing_packages)}")
        print(f"   💡 Run: pip install -r {requirements_file}")
        return False
    else:
        print(f"   ✅ All packages installed")
        return True

def main():
    """Run configuration checks"""
    print("🔍 Mimicker AI Configuration Checker\n")
    
    checks = []
    
    # Check project structure
    print("📁 Checking project structure...")
    structure_checks = [
        ("backend/app.py", "Backend main file"),
        ("backend/requirements.txt", "Backend requirements"),
        ("MCP_server/MCP_mimic/main.py", "MCP server main file"),
        ("MCP_server/MCP_mimic/requirements.txt", "MCP server requirements"),
        ("client/package.json", "Frontend package.json"),
        ("start_all.bat", "Startup script"),
    ]
    
    structure_ok = True
    for file_path, description in structure_checks:
        if not check_file_exists(file_path, description):
            structure_ok = False
    
    checks.append(("Project Structure", structure_ok))
    
    # Check environment files
    print("\n🔧 Checking environment configuration...")
    
    backend_env_ok = check_env_file("backend/.env", [
        "MONGODB_URI", "JWT_SECRET_KEY", "MCP_SERVER_URL"
    ])
    checks.append(("Backend Environment", backend_env_ok))
    
    mcp_env_ok = check_env_file("MCP_server/MCP_mimic/.env", [
        "GEMINI_API_KEY"
    ])
    checks.append(("MCP Environment", mcp_env_ok))
    
    # Check Python dependencies
    print("\n📦 Checking Python dependencies...")
    
    backend_deps_ok = check_python_packages("backend/requirements.txt")
    checks.append(("Backend Dependencies", backend_deps_ok))
    
    mcp_deps_ok = check_python_packages("MCP_server/MCP_mimic/requirements.txt")
    checks.append(("MCP Dependencies", mcp_deps_ok))
    
    # Check Node.js dependencies
    print("\n📦 Checking Node.js dependencies...")
    if os.path.exists("client/node_modules"):
        print("   ✅ Node modules installed")
        frontend_deps_ok = True
    else:
        print("   ❌ Node modules missing")
        print("   💡 Run: cd client && npm install")
        frontend_deps_ok = False
    
    checks.append(("Frontend Dependencies", frontend_deps_ok))
    
    # Summary
    print("\n" + "="*50)
    print("📊 CONFIGURATION CHECK SUMMARY")
    print("="*50)
    
    passed = 0
    for check_name, result in checks:
        status = "✅ OK" if result else "❌ FAIL"
        print(f"{status} - {check_name}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{len(checks)} checks passed")
    
    if passed == len(checks):
        print("\n🎉 Configuration is complete! You can now start the application.")
        print("\nTo start all services:")
        print("   Windows: start_all.bat")
        print("   Manual: Run backend, MCP server, and frontend in separate terminals")
    else:
        print("\n⚠️  Configuration incomplete. Please fix the issues above.")
        print("\nSetup checklist:")
        print("1. Copy .env.example files and fill in your values")
        print("2. Install Python dependencies: pip install -r requirements.txt")
        print("3. Install Node.js dependencies: cd client && npm install")
        print("4. Make sure MongoDB is running")

if __name__ == "__main__":
    main()