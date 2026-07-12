import os
import sys
import subprocess

def run_build():
    """Installs PyInstaller if missing and compiles run.py to MonitorAI.exe."""
    print("====================================================")
    print("           MonitorAI Executable Builder             ")
    print("====================================================")

    # 1. Install PyInstaller if not already present
    try:
        import PyInstaller
        print("[+] PyInstaller is already installed.")
    except ImportError:
        print("[!] PyInstaller not found. Installing via pip...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("[+] PyInstaller successfully installed!")
        except Exception as e:
            print(f"[ERROR] Failed to install PyInstaller: {e}")
            sys.exit(1)

    # 2. Compile application into a single file executable
    # On Windows, PyInstaller separates source/target data directories using a semicolon (;)
    print("\n[+] Compiling run.py into standalone executable MonitorAI.exe...")
    build_cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",
        "--name=MonitorAI",
        "--add-data=app/templates;app/templates",
        "--add-data=app/static;app/static",
        "run.py"
    ]
    
    try:
        subprocess.check_call(build_cmd)
        print("\n====================================================")
        print("[SUCCESS] Standalone Executable created successfully!")
        print(f"You can find the application 'MonitorAI.exe' inside: {os.path.join(os.getcwd(), 'dist')}")
        print("====================================================")
    except Exception as e:
        print(f"\n[ERROR] Failed to compile application using PyInstaller: {e}")
        sys.exit(1)

if __name__ == '__main__':
    run_build()
