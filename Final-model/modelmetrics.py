import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns
import cv2
import os
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_recall_fscore_support
from sklearn.preprocessing import label_binarize
from sklearn.metrics import roc_curve, precision_recall_curve
import random

# Image Augmentation: Apply transformations to make classification harder
def modify_image(image):
    """Applies random transformations to decrease model accuracy."""
    
    # Convert to OpenCV format (uint8, 0-255)
    image = (image * 255).astype(np.uint8)
    
    # Randomly apply different transformations
    if random.random() < 0.5:  
        image = cv2.GaussianBlur(image, (5, 5), 0)  # Apply blur
        
    if random.random() < 0.5:  
        image = cv2.convertScaleAbs(image, alpha=0.5, beta=0)  # Reduce brightness
        
    if random.random() < 0.5:  
        image = cv2.convertScaleAbs(image, alpha=1, beta=-50)  # Reduce contrast
        
    if random.random() < 0.5:  
        angle = random.randint(-20, 20)
        (h, w) = image.shape[:2]
        M = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)
        image = cv2.warpAffine(image, M, (w, h))  # Apply random rotation
    
    if random.random() < 0.5:  
        # Add salt & pepper noise
        noise = np.random.randint(0, 255, image.shape, dtype=np.uint8)
        mask = np.random.choice([0, 1, 2], size=image.shape[:2], p=[0.9, 0.05, 0.05])
        image[mask == 1] = 255  # Salt
        image[mask == 2] = 0    # Pepper
    
    return image / 255.0  # Normalize again (0-1)

# Use your existing dataset loading function
def load_data(dataset_dir, img_height=400, img_width=400, num_classes=29, modify=False):
    """Loads dataset and applies modifications if modify=True."""
    X, y = [], []
    
    if not os.path.exists(dataset_dir):
        raise FileNotFoundError(f"Dataset directory not found: {dataset_dir}")

    print("Available directories:", os.listdir(dataset_dir))

    total_images = 0
    folder_mapping = {folder.upper(): folder for folder in os.listdir(dataset_dir)}

    class_mapping = {
        "A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7,
        "I": 8, "J": 9, "K": 10, "L": 11, "M": 12, "N": 13, "O": 14, "P": 15,
        "Q": 16, "R": 17, "S": 18, "T": 19, "U": 20, "V": 21, "W": 22, "X": 23,
        "Y": 24, "Z": 25, "SPACE": 26, "BACKSPACE": 27, "NEXT": 28
    }

    for folder_name_upper, label in class_mapping.items():
        if folder_name_upper in folder_mapping:
            actual_folder_name = folder_mapping[folder_name_upper]
            folder_path = os.path.join(dataset_dir, actual_folder_name)

            if os.path.isdir(folder_path):
                files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

                for file_name in files:
                    file_path = os.path.join(folder_path, file_name)
                    try:
                        img = tf.keras.utils.load_img(
                            file_path,
                            target_size=(img_height, img_width),
                            color_mode="rgb"
                        )
                        img_array = tf.keras.utils.img_to_array(img) / 255.0
                        
                        if modify:
                            img_array = modify_image(img_array)  # Apply modifications
                        
                        X.append(img_array)
                        y.append(label)
                        total_images += 1
                    except Exception as e:
                        print(f"Error loading image {file_path}: {e}")

    if total_images == 0:
        raise ValueError("No images were loaded. Check the dataset directory and file formats.")

    return np.array(X), np.array(y)

# Set dataset directory
dataset_dir = "C:\\Users\\wissa\\Desktop\\Final-model\\A-Z"

# Load modified test dataset
print("Loading modified test data...")
X_test, y_test = load_data(dataset_dir, modify=True)  # Apply modifications
y_test = tf.keras.utils.to_categorical(y_test, num_classes=29)
y_test_labels = np.argmax(y_test, axis=1)

print(f"Data Loaded: X_test shape: {X_test.shape}, y_test shape: {y_test.shape}")

# Load trained model
model = tf.keras.models.load_model("sign_language_model_v29.h5")

# Model Predictions
y_pred_probs = model.predict(X_test)
y_pred_labels = np.argmax(y_pred_probs, axis=1)

# Compute Metrics
accuracy = accuracy_score(y_test_labels, y_pred_labels)
precision, recall, f1, _ = precision_recall_fscore_support(y_test_labels, y_pred_labels, average='weighted')
conf_matrix = confusion_matrix(y_test_labels, y_pred_labels)

# Print Metrics
print(f"\nModified Data Model Evaluation:")
print(f"Accuracy: {accuracy * 100:.2f}%")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1-Score: {f1:.2f}\n")
print("Classification Report:\n", classification_report(y_test_labels, y_pred_labels))

# Display Confusion Matrix
plt.figure(figsize=(10, 7))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=list(range(29)), yticklabels=list(range(29)))
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.title("Confusion Matrix")
plt.show()

# Plot Per-Class Accuracy
class_accuracies = conf_matrix.diagonal() / conf_matrix.sum(axis=1)
plt.figure(figsize=(10, 5))
plt.bar(range(29), class_accuracies, color='red')
plt.xlabel("Alphabet Class (A-Z, SPACE, BACKSPACE, NEXT)")
plt.ylabel("Accuracy")
plt.title("Per-Class Classification Accuracy")
plt.xticks(range(29), [chr(65 + i) if i < 26 else ["SPACE", "BACKSPACE", "NEXT"][i - 26] for i in range(29)], rotation=45)
plt.ylim(0, 1)
plt.show()



# ROC & Precision-Recall Curves
y_test_bin = label_binarize(y_test_labels, classes=range(29))  # Convert to binary format
plt.figure(figsize=(12, 6))

# ROC Curve
plt.subplot(1, 2, 1)
for i in range(29):
    fpr, tpr, _ = roc_curve(y_test_bin[:, i], y_pred_probs[:, i])
    plt.plot(fpr, tpr, label=f'Class {chr(65+i) if i < 26 else ["SPACE", "BACKSPACE", "NEXT"][i-26]}')
plt.plot([0, 1], [0, 1], 'k--')  # Random chance line
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")
plt.legend(loc="lower right")

# Precision-Recall Curve
plt.subplot(1, 2, 2)
for i in range(29):
    precision, recall, _ = precision_recall_curve(y_test_bin[:, i], y_pred_probs[:, i])
    plt.plot(recall, precision, label=f'Class {chr(65+i) if i < 26 else ["SPACE", "BACKSPACE", "NEXT"][i-26]}')
plt.xlabel("Recall")
plt.ylabel("Precision")
plt.title("Precision-Recall Curve")
plt.legend(loc="lower left")

plt.show()