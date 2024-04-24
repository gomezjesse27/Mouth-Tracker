import pandas as pd
from sklearn.decomposition import PCA
from sklearn.multioutput import MultiOutputRegressor
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np
import joblib
from config import *

# Load the transformed training data
data = pd.read_csv('./training_set_pca.csv')
print(data.head())
# Separate the features and the target variables
X_pca = data.iloc[:, :-TARGET_COUNT]
y = data.iloc[:, -TARGET_COUNT:]

# Load the PCA model
pca = joblib.load('pca_model.pkl')

# Train a linear regression model to predict the multiple outputs
regression_model = MultiOutputRegressor(LinearRegression()).fit(X_pca, y)
# Save the model to disk
joblib.dump(regression_model, 'lr_model.pkl')
