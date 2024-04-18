import pandas as pd
from sklearn.decomposition import PCA
from sklearn.multioutput import MultiOutputRegressor
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np
import joblib

# Load the training data
data = pd.read_csv('./training_set.csv')

print(data.head())

# Separate the features and the target variable\
num_target_vars = 2
X = data.iloc[:, :-num_target_vars]
y = data[['target0', 'target1']]

# Perform PCA on the features
pca = PCA(n_components=5)  # Choose the number of components you want to keep
X_pca = pca.fit_transform(X)
# Save the model to disk
joblib.dump(pca, 'pca_model.pkl')

# Plot percentages of explained variance
per_var = np.round(pca.explained_variance_ratio_* 100, decimals=1)
# labels = ['PC' + str(x) for x in range(1, len(per_var)+1)]
# plt.bar(x=range(1, len(per_var)+1), height=per_var, tick_label=labels)
# plt.ylim(0, 100)  # Set the y-axis limits
# plt.ylabel('Percentage of Explained Variance')
# plt.xlabel('Principal Component')
# plt.title('Scree Plot')
#plt.show()
print(f"Total variance explained by these {len(per_var)} components: {sum(per_var)}%")

# Train a linear regression model to predict the multiple outputs
regression_model = MultiOutputRegressor(LinearRegression()).fit(X_pca, y)
# Save the model to disk
joblib.dump(regression_model, 'multioutput_linear_regression_model.pkl')
