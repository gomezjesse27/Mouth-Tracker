"""
Created 3/27/2024
Main Script for CBMT Project
"""
import subprocess
import os
import sys
from config import *

# Path to your virtual environment's Python interpreter
# If you don't want to use a virtual environment, you can comment out this line
venv_python_path = os.path.join(os.getcwd(), 'venv', 'Scripts', 'python')

def run_script(script_name):
    print(f"Running {script_name}")
    result = subprocess.run([venv_python_path, f"./{script_name}"])
    if result.returncode != 0:
        print(f"Error running {script_name}, exiting.")
        sys.exit(1)

print_config()
run_script("data_collection.py")
run_script("data_preprocessing_pca.py")
run_script("modeling_lr.py")
run_script("prediction_lr.py")

print("Goodbye!")