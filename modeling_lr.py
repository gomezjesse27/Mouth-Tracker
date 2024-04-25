import pandas as pd
from sklearn.decomposition import PCA
from sklearn.metrics import mean_squared_error
from sklearn.multioutput import MultiOutputRegressor
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from config import *

# Load the transformed training data
data = pd.read_csv('./training_set_pca.csv')
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)
test_data.to_csv('./test_set_pca.csv', index=False)
print(train_data.head())
# Separate the features and the target variables
X_pca = train_data.iloc[:, :-TARGET_COUNT]
y = train_data.iloc[:, -TARGET_COUNT:]

# Load the PCA model
pca = joblib.load('pca_model.pkl')

# Train a linear regression model to predict the multiple outputs
regression_model = MultiOutputRegressor(LinearRegression()).fit(X_pca, y)
# Save the model to disk
joblib.dump(regression_model, 'lr_model.pkl')

### testing ###########
# Separate the features and the target variables from the test data
X_test_pca = test_data.iloc[:, :-TARGET_COUNT]
y_test = test_data.iloc[:, -TARGET_COUNT:]

# Use the trained model to make predictions on the test data
y_pred = regression_model.predict(X_test_pca)

# Evaluate the performance of the model
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error on test data: {mse}')