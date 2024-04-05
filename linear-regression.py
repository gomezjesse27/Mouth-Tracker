import pandas as pd
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np
import joblib

# Load the training data
data = pd.read_csv('training_set.csv')

print(data.head())

# Separate the features and the target variable
X = data.iloc[:, :-1]
y = data['target0']

# Perform PCA on the features
pca = PCA(n_components=5)  # Choose the number of components you want to keep
X_pca = pca.fit_transform(X)
# Save the model to disk
joblib.dump(pca, 'pca_model.pkl')

# Plot percentages of explained variance
per_var = np.round(pca.explained_variance_ratio_* 100, decimals=1)
labels = ['PC' + str(x) for x in range(1, len(per_var)+1)]
plt.bar(x=range(1, len(per_var)+1), height=per_var, tick_label=labels)
plt.ylim(0, 100)  # Set the y-axis limits
plt.ylabel('Percentage of Explained Variance')
plt.xlabel('Principal Component')
plt.title('Scree Plot')
#plt.show()
print(f"Total variance explained by these {len(per_var)} components: {sum(per_var)}%")

# Train a linear regression model
model = LinearRegression()
model.fit(X_pca, y)
# Save the model to disk
joblib.dump(model, 'linear_regression_model.pkl')


# Predict the target variable for a new datapoint
# new_datapoint = [[0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]]  # Replace with your new datapoint
# new_datapoint_pca = pca.transform(new_datapoint)
# prediction = model.predict(new_datapoint_pca)

# print('Predicted target:', prediction)