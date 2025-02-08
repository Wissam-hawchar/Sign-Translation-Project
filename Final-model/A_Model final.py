import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import CategoricalCrossentropy
from sklearn.model_selection import train_test_split

base_dir = "C:\\Users\\wissa\\Desktop\\Final-model"
dataset_dir = os.path.join(base_dir, "A-Z")

img_height, img_width = 400, 400
num_classes = 29 

class_mapping = {
    "A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7,
    "I": 8, "J": 9, "K": 10, "L": 11, "M": 12, "N": 13, "O": 14, "P": 15,
    "Q": 16, "R": 17, "S": 18, "T": 19, "U": 20, "V": 21, "W": 22, "X": 23,
    "Y": 24, "Z": 25, "SPACE": 26, "BACKSPACE": 27, "NEXT": 28
}

def load_data(dataset_dir):
    X, y = [], []

    if not os.path.exists(dataset_dir):
        raise FileNotFoundError(f"Dataset directory not found: {dataset_dir}")

    print("Available directories:", os.listdir(dataset_dir))

    total_images = 0
    folder_mapping = {folder.upper(): folder for folder in os.listdir(dataset_dir)}

    for folder_name_upper, label in class_mapping.items():
        if folder_name_upper in folder_mapping:
            actual_folder_name = folder_mapping[folder_name_upper]
            folder_path = os.path.join(dataset_dir, actual_folder_name)

            print(f"Processing folder: {actual_folder_name}")

            if os.path.isdir(folder_path):
                files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                print(f"Found {len(files)} images in {actual_folder_name}")

                for file_name in files:
                    file_path = os.path.join(folder_path, file_name)
                    try:
                        img = tf.keras.utils.load_img(
                            file_path,
                            target_size=(img_height, img_width),
                            color_mode="rgb"
                        )
                        img_array = tf.keras.utils.img_to_array(img) / 255.0
                        X.append(img_array)
                        y.append(label)
                        total_images += 1
                    except Exception as e:
                        print(f"Error loading image {file_path}: {e}")
        else:
            print(f"Warning: Folder {folder_name_upper} not found in dataset")

    print(f"Total images loaded: {total_images}")

    if total_images == 0:
        raise ValueError("No images were loaded. Check the dataset directory and file formats.")

    return np.array(X), np.array(y)

try:
    print("Starting data loading...")
    X, y = load_data(dataset_dir)
    print(f"Data loaded successfully. X shape: {X.shape}, y shape: {y.shape}")
except Exception as e:
    print(f"Error loading data: {e}")
    raise

y = tf.keras.utils.to_categorical(y, num_classes=num_classes)

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Training set shape: {X_train.shape}")
print(f"Validation set shape: {X_val.shape}")

model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(img_height, img_width, 3)),
    MaxPooling2D(pool_size=(2, 2)),
    Conv2D(32, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Conv2D(16, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Conv2D(16, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(96, activation='relu'),
    Dropout(0.4),
    Dense(64, activation='relu'),
    Dense(num_classes, activation='softmax')
])

model.compile(
    optimizer=Adam(learning_rate=0.001),
    loss=CategoricalCrossentropy(),
    metrics=['accuracy']
)

model.summary()

history = model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    epochs=15,
    batch_size=16
)

model.save("sign_language_model_v29.h5")

final_train_accuracy = history.history['accuracy'][-1]
final_val_accuracy = history.history['val_accuracy'][-1]
print(f"\nFinal Training Accuracy: {final_train_accuracy:.4f}")
print(f"Final Validation Accuracy: {final_val_accuracy:.4f}")
