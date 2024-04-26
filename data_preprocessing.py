import pandas as pd
from sklearn.decomposition import PCA
from sklearn.multioutput import MultiOutputRegressor
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np
import joblib
from config import *

done = False

def data_preprocessing_init():
    global done
    # Load the training data
    data = pd.read_csv('./training_set.csv')

    print(data.head())

    # Separate the features and the target variables
    X = data.iloc[:, :-TARGET_COUNT]
    y = data.iloc[:, -TARGET_COUNT:]

    # Perform PCA on the features
    pca = PCA(n_components=5)  # Choose the number of components you want to keep
    X_pca = pca.fit_transform(X)

    # Save the PCA model to disk
    joblib.dump(pca, 'pca_model.pkl')
    # Save a transformed version of training_set.csv
    X_pca_df = pd.DataFrame(X_pca)
    X_pca_df = pd.concat([X_pca_df, y], axis=1)
    X_pca_df.to_csv('training_set_pca.csv', index=False)

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
    done = True

def data_preprocessing_update(screen, events):
    global done
    return done
