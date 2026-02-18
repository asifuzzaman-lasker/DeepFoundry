import subprocess
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: deepfoundry run app.py")
        sys.exit(1)

    command = sys.argv[1]
    if command == "run":
        if len(sys.argv) < 3:
            print("Please specify the file to run, e.g. deepfoundry run app.py")
            sys.exit(1)
        app_file = sys.argv[2]
        subprocess.run(["streamlit", "run", app_file])
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
