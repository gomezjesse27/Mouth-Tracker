import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, LeakyReLU, Input
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau, TensorBoard
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Set consistent resolution across the script
downsized_dimension = 64  

# Load and preprocess data
data = pd.read_csv('training_set_cnn.csv')
X = data.iloc[:, :-2].values.reshape(-1, downsized_dimension, downsized_dimension, 1)
y = data.iloc[:, -2:].values
X = X / 255.0  # Normalize pixel values

# Split data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.4, random_state=42)

# Image data augmentation for training
train_datagen = ImageDataGenerator(
    rotation_range=10,
    width_shift_range=0.1,
    height_shift_range=0.1,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)
val_datagen = ImageDataGenerator()  # Validation data without augmentation

# Create data generators
train_generator = train_datagen.flow(X_train, y_train, batch_size=64)
val_generator = val_datagen.flow(X_val, y_val, batch_size=64)

# Define CNN model structure
model = Sequential([
    Input(shape=(downsized_dimension, downsized_dimension, 1)),
    Conv2D(32, (3, 3), padding='same'),
    LeakyReLU(negative_slope=0.1),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), padding='same'),
    LeakyReLU(negative_slope=0.1),
    MaxPooling2D((2, 2)),
    Conv2D(128, (3, 3), padding='same'),
    LeakyReLU(negative_slope=0.1),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(256),
    LeakyReLU(negative_slope=0.1),
    Dropout(0.5),
    Dense(128),
    LeakyReLU(negative_slope=0.1),
    Dense(2, activation='sigmoid')
])

# Compile the model with appropriate optimizer, loss, and metrics
model.compile(optimizer=Adam(learning_rate=0.00001), loss='mean_squared_error', metrics=['mean_squared_error'])

# Setup callbacks for model optimization
tensorboard_callback = TensorBoard(log_dir='./logs', histogram_freq=1, write_graph=True, write_images=True)
early_stopping = EarlyStopping(monitor='val_loss', patience=10, verbose=1, mode='min', restore_best_weights=True)
model_checkpoint = ModelCheckpoint('best_model.keras', save_best_only=True, verbose=1, mode='min')
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=3, verbose=1, mode='min', min_lr=1e-6)

# Fit the model
history = model.fit(
    train_generator,
    steps_per_epoch=int(len(X_train) / 32),
    validation_data=val_generator,
    validation_steps=int(len(X_val) / 32),
    epochs=60,
    callbacks=[tensorboard_callback, early_stopping, model_checkpoint, reduce_lr],
    shuffle=True
)

# Save the model
model.save('cnn_model.h5')

# Plotting the training and validation loss and MSE
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(history.history['mean_squared_error'], label='Train MSE')
plt.plot(history.history['val_mean_squared_error'], label='Validation MSE')
plt.title('Model MSE')
plt.ylabel('MSE')
plt.xlabel('Epoch')
plt.legend(loc='upper left')

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(loc='upper right')
plt.show()
