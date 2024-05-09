import pandas as pd
from sklearn.decomposition import PCA
from sklearn.metrics import mean_squared_error
from sklearn.multioutput import MultiOutputRegressor
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np
import joblib
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split
from config import *

done = False

def modeling_ann_init():
    global done
    done = False
    # Load the transformed training data
    data = pd.read_csv('./training_set_pca.csv')
    train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)
    test_data.to_csv('./test_set_pca.csv', index=False)
    print(train_data.head())
    # Separate the features and the target variables
    X_pca = train_data.iloc[:, :-TARGET_COUNT]
    y = train_data.iloc[:, -TARGET_COUNT:]

    # number of input and outputs respectively
    n_features = X_pca.shape[1]
    n_targets = y.shape[1]

    model = Sequential()
    model.add(Dense(20, input_dim=n_features, activation='relu'))
    model.add(Dense(n_targets, activation='linear')) # Output layer

    # Compile
    model.compile(loss='mean_squared_error', optimizer='adam')
    # Train
    model.fit(X_pca, y, epochs=50, batch_size=10)
    # Save
    model.save('ann_model.h5')
    done = True

def modeling_ann_update(screen, events):
    global done
    return done