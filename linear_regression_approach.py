import subprocess
import os

# Path to your virtual environment's Python interpreter
# If you don't want to use a virtual environment, you can comment out this line
venv_python_path = os.path.join(os.getcwd(), 'venv', 'Scripts', 'python')

# Run training-set-maker.py
print("Running training-set-maker.py")
subprocess.run([venv_python_path, "./training-set-maker/training-set-maker.py"])

# Run pca_and_lin_reg_modeling.py
print("Running pca_and_lin_reg_modeling.py")
subprocess.run([venv_python_path, "./pca_and_lin_reg_modeling.py"])

# Run lin_reg_prediction.py
print("Running lin_reg_prediction.py")
subprocess.run([venv_python_path, "./lin_reg_prediction.py"])

print("Goodbye!")