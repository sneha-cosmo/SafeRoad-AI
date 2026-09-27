
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
