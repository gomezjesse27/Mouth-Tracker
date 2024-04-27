import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from config import *

def modeling_cnn_init():
    global done
    done = False

    # Load the training data
    data = pd.read_csv('./training_set.csv')
    
    # Ensure that data contains the correct number of columns expected as per RESOLUTION and TARGET_COUNT
    if len(data.columns) != RESOLUTION * RESOLUTION + TARGET_COUNT:
        print("Error: Data does not match the expected format.")
        done = True
        return

    # Split the data
    X = data.iloc[:, :-TARGET_COUNT].values
    y = data.iloc[:, -TARGET_COUNT:].values

    # Check if y contains more than one column and it's not already in the correct categorical format
    if y.ndim == 1 or y.shape[1] == 1:
        y = to_categorical(y)  # This assumes y contains class indices as integers from 0 to num_classes-1

    num_classes = y.shape[1]

    # Reshape X to fit the model's input requirements: (num_samples, RESOLUTION, RESOLUTION, 1)
    X = X.reshape(-1, RESOLUTION, RESOLUTION, 1)

    # Normalize the pixel values
    X = X.astype('float32') / 255.0

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Define the CNN model architecture
    
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(RESOLUTION, RESOLUTION, 1)),
        MaxPooling2D(2, 2),# Max pooling layer
        Conv2D(64, (3, 3), activation='relu'), #2 convolutional layers 
        MaxPooling2D(2, 2),
        Flatten(),# flatten the 3D output to 1D
        Dense(128, activation='relu'), # 1 dense layer
        Dropout(0.5),
        Dense(num_classes, activation='softmax')  # number of classes here
        #softmax activation function instead of sigmoid
    ])

    # Compile the model
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    # Train the model
    model.fit(X_train, y_train, epochs=15, batch_size=64, validation_data=(X_test, y_test))

    # Save the model to disk
    model.save('cnn_model.h5')

    print("Model trained and saved successfully.")
    done = True

def modeling_cnn_update(screen, events, caps):
    global done
    return done
