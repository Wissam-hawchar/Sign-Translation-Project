```markdown
# Sign Translation Software

This project is a Sign Language Translation System that recognizes and translates American Sign Language (ASL) alphabet gestures into text using computer vision and deep learning. It leverages MediaPipe for hand landmark detection and a Convolutional Neural Network (CNN) for classification. A Tkinter-based Python application is developed for real-time sign recognition, and a mobile application extends the functionality with text-to-sign, audio-to-sign, and an ASL dictionary.

## 🚀 Features
- 🎥 Real-time ASL alphabet recognition using computer vision.
- 🖐️ MediaPipe-based hand landmark detection for efficient processing.
- 🧠 CNN-based classification model for gesture recognition.
- 🖥️ Tkinter GUI application for user-friendly interaction.
- 📱 Mobile application with:
  - 📝 Text-to-sign translation
  - 🎙️ Audio-to-sign conversion
  - 📖 ASL dictionary for learning gestures.
- 📊 Hierarchical classification approach to improve accuracy.
- 🌎 Robustness under different lighting conditions and hand positioning.


## 📱 Mobile Application
The mobile version of the application supports text-to-sign and audio-to-sign features.  
The source code can be found in the [`final-app/`]directory.

## 📊 Model Performance
The CNN model was trained on ASL alphabet gestures and evaluated using:
- ✅ Accuracy: 85.21%
- 🎯 Precision: 87%
- 📈 Recall: 85%
- 🔄 F1-score: 85%

Despite good performance under controlled conditions, the model faces challenges with varying lighting and background complexity.

## 🏗️ Future Enhancements
🔹 Expanding the dataset for better generalization.  
🔹 Improving model accuracy with deeper architectures.  
🔹 Extending support for full sign language words/sentences.  
🔹 Optimizing for low-power mobile devices.  

