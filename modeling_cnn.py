import pandas as pd
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, LeakyReLU, Input
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau, TensorBoard
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
from config import RESOLUTION, FEATURE_COLUMNS, LABEL_COLUMNS, BATCH_SIZE, ALGORITHM, Algorithms

def modeling_cnn_init():
    # Import data
    global done
    data = pd.read_csv('training_set.csv')
    X = data.iloc[:, FEATURE_COLUMNS].values.reshape(-1, RESOLUTION, RESOLUTION, 1) / 255.0
    y = data.iloc[:, LABEL_COLUMNS].values

    # Split data into training and validation sets
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.4, random_state=42)

    # Create data generators for training and validation
    train_datagen = ImageDataGenerator(
        rotation_range=10,
        width_shift_range=0.1,
        height_shift_range=0.1,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    val_datagen = ImageDataGenerator()

    train_generator = train_datagen.flow(X_train, y_train, batch_size=BATCH_SIZE)
    val_generator = val_datagen.flow(X_val, y_val, batch_size=BATCH_SIZE)

    # Define the CNN model
    model = Sequential([
        Input(shape=(RESOLUTION, RESOLUTION, 1)),
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
        Dense(y.shape[1], activation='sigmoid')
    ])

    # Compile the model
    model.compile(optimizer=Adam(learning_rate=0.0001), loss='mean_squared_error', metrics=['mean_squared_error'])

    # Setup callbacks
    callbacks = [
        TensorBoard(log_dir='./logs', histogram_freq=1, write_graph=True, write_images=True),
        EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True),
        ModelCheckpoint('best_model.keras', save_best_only=True),
        ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=3, min_lr=1e-6)
    ]

    # Fit the model
    history = model.fit(
        train_generator,
        steps_per_epoch=len(X_train) // BATCH_SIZE,
        validation_data=val_generator,
        validation_steps=len(X_val) // BATCH_SIZE,
        epochs=60,
        callbacks=callbacks,
        shuffle=True
    )

    # Save the trained model
    model.save('cnn_model.h5')
    done = True
    # Plot training and validation metrics
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
    

def modeling_cnn_update(screen, events, cap):
    global done
    
    return done