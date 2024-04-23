import subprocess
import os
import sys

# Path to your virtual environment's Python interpreter
# If you don't want to use a virtual environment, you can comment out this line
venv_python_path = os.path.join(os.getcwd(), 'venv', 'Scripts', 'python')

def run_script(script_name):
    print(f"Running {script_name}")
    result = subprocess.run([venv_python_path, f"./{script_name}"])
    if result.returncode != 0:
        print(f"Error running {script_name}, exiting.")
        sys.exit(1)

# Run training-set-maker.py
run_script("training-set-maker.py")

# Run pca_and_lin_reg_modeling.py
run_script("pca_and_lin_reg_modeling.py")

# Run lin_reg_prediction.py
run_script("lin_reg_prediction.py")

print("Goodbye!")