
# SafeRoad AI

## CNN-Based Pothole Detection and Intelligent Road Risk Analysis

SafeRoad AI is an AI-based road condition detection system that uses a Convolutional Neural Network (CNN) to identify whether a road image contains a pothole or represents a normal road.

The system also provides a visual severity level, risk level, and safety recommendation based on the detected road condition.

---

## Project Overview

Road potholes can create safety risks for vehicles and road users. Manual identification of potholes over large road networks can be time-consuming.

SafeRoad AI aims to automate the first stage of road-condition inspection by analyzing road images using deep learning.

### Main Functions

- Detect potholes from road images
- Classify roads as Normal or Pothole
- Display prediction confidence
- Estimate visual severity
- Determine road risk level
- Provide a safety recommendation
- Provide an interactive web interface using Streamlit

---

## System Architecture

```text
Road Image
     ↓
Image Preprocessing
     ↓
MobileNetV2 CNN
     ↓
Normal / Pothole
     ↓
Visual Severity
     ↓
Risk Level
     ↓
Safety Recommendation

Technologies Used
Python
TensorFlow
Keras
MobileNetV2
NumPy
Pillow
Streamlit
Git & GitHub
Dataset

The project uses a binary road-image dataset containing:

2,500 Normal road images
2,500 Pothole images
Total: 5,000 images

The images are divided into training, validation, and testing sets.

Machine Learning Model

The system uses MobileNetV2 with transfer learning.

The pretrained MobileNetV2 feature extractor is used to learn useful visual features from road images.

A classification head is added:

MobileNetV2
     ↓
Global Average Pooling
     ↓
Dense Layer (128 neurons)
     ↓
Dropout
     ↓
Sigmoid Output
     ↓
Normal / Pothole

The model uses:

Input size: 224 × 224 pixels
Optimizer: Adam
Loss function: Binary Cross-Entropy
Output activation: Sigmoid
Training epochs: 10
Model Performance

The trained model achieved approximately:

Metric	Result
Training Accuracy	98.35%
Validation Accuracy	95.97%
Test Accuracy	97.6%

The test classification results showed approximately 97% precision, recall, and F1-score for both classes.

Intelligent Risk Analysis

After pothole detection, SafeRoad AI provides an additional road-risk analysis layer.

Visual Severity

The current prototype uses three levels:

Low – small or limited-looking road damage
Medium – noticeable road damage
High – large or extensive-looking road damage
Risk Levels
Low Severity
     ↓
Low Risk

Medium Severity
     ↓
Medium Risk

High Severity
     ↓
High Risk
Example Recommendations

Low Risk

Proceed with normal caution.

Medium Risk

Reduce speed and proceed carefully.

High Risk

Reduce speed and avoid the pothole if safe.

Streamlit Application

SafeRoad AI provides a web interface where the user can upload a road image.

The application displays:

Road Condition : Pothole
Confidence     : 99.77%
Visual Severity: Medium
Risk Level     : Medium

Recommendation:
Reduce speed and proceed carefully.
Project Structure
SafeRoad-AI/
│
├── app.py
├── SafeRoad_AI_Model.keras
├── requirements.txt
├── README.md
└── .gitignore
Installation

Clone the repository:

git clone https://github.com/sneha-cosmo/SafeRoad-AI.git

Move into the project directory:

cd SafeRoad-AI

Install the required Python packages:

pip install -r requirements.txt
Run the Application

Start the Streamlit application using:

python -m streamlit run app.py

The application will open in your web browser.

Upload a road image to receive the pothole detection result and road-risk analysis.

Limitations
The CNN is trained for binary classification: Normal and Pothole.
The current dataset does not contain dedicated severity labels.
Therefore, visual severity is an additional rule-based assessment rather than a separately trained severity model.
Image-based severity should not be interpreted as a physical measurement of pothole depth.
Performance may vary for images with different lighting, camera angles, road surfaces, or environmental conditions.
Future Improvements

Possible future improvements include:

Real-time pothole detection using a camera
GPS-based pothole location mapping
Pothole severity dataset and dedicated severity model
Object detection for locating multiple potholes
Pothole tracking and deterioration analysis
Mobile application integration
Road-condition monitoring dashboard
Integration with vehicle safety systems
Project Goal

The goal of SafeRoad AI is to demonstrate how computer vision and deep learning can be used as a foundation for automated road-condition monitoring and intelligent road-risk analysis.


### Why we're doing this

Your GitHub repository currently contains the **actual working model and application**, but someone visiting the repository needs to understand:

**What is it? → How does it work? → What model did you use? → How accurate is it? → How do I run it?**

That's exactly what this README provides.

### One important point

I deliberately wrote:

> **"visual severity"**

instead of claiming that the system measures actual pothole depth. Your current dataset has **Normal/Pothole labels**, not Low/Medium/High severity labels, so this keeps your project technically honest.

---

After saving `README.md`, **don't commit yet**.

Run:

```powershell
git status
