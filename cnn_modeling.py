import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Dropout
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau

import matplotlib.pyplot as plt

# loading the training data
data = pd.read_csv('training_set_cnn.csv')
X = data.iloc[:, :-1].values.reshape(-1, 24, 24, 1)  # Reshape for CNN, assuming images are 24x24 pixels
y = data.iloc[:, -1].values

# the CNN architecture
# model = Sequential([
#     Conv2D(32, (3, 3), activation='relu', input_shape=(24, 24, 1)),
#     MaxPooling2D((2, 2)),
#     Conv2D(64, (3, 3), activation='relu'),
#     MaxPooling2D((2, 2)),
#     Flatten(),
#     Dense(128, activation='relu'),
#     Dense(1, activation='sigmoid')  
# ])


model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(24, 24, 1)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Conv2D(128, (3, 3), activation='relu'),  # added layer
    MaxPooling2D((2, 2)),                   # added layer
    Flatten(),
    Dense(256, activation='relu'),          # increased size
    Dropout(0.5),                           # dropout for regularization
    Dense(128, activation='relu'),          # another... you guessed it ... layer
    Dense(1, activation='sigmoid')
])

# Complie
model.compile(optimizer=Adam(), loss='binary_crossentropy', metrics=['accuracy'])

# Train
# history = model.fit(X, y, epochs=5, batch_size=32, validation_split=0.2)

# Callbacks
early_stopping = EarlyStopping(monitor='val_loss', patience=5, verbose=1, mode='min', restore_best_weights=True)
model_checkpoint = ModelCheckpoint('best_model.keras', monitor='val_loss', save_best_only=True, verbose=1, mode='min')
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=2, verbose=1, mode='min', min_lr=1e-6)

# Training the model
history = model.fit(
    X, y,
    epochs=20,
    batch_size=64,
    validation_split=0.2,
    callbacks=[early_stopping, model_checkpoint, reduce_lr],
    shuffle=True  
)

# Save to disk
model.save('cnn_model.h5')

# plotting the metrics
plt.plot(history.history['accuracy'], label='Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(loc='upper left')
plt.show()
