# AI-Based Real-Time Attention Monitoring System

## Abstract

This project presents a real-time, web-based attention monitoring system that evaluates user engagement using computer vision. By integrating posture analysis and facial behavior tracking, the system estimates cognitive states such as focus, distraction, and drowsiness. The solution operates without any training dataset, relying on rule-based inference over pose and facial landmarks.

## Problem Statement

Maintaining attention during prolonged screen interaction is a critical challenge in educational and professional environments. Existing solutions often require intrusive hardware or large datasets. This project aims to develop a lightweight, real-time system that can monitor attention using only a standard webcam.


## Objectives

* To detect and analyze human posture in real time
* To identify facial behavioral cues such as eye closure and head direction
* To compute an attention score based on multiple parameters
* To classify user cognitive states dynamically
* To present results through an interactive web interface


## System Architecture

Webcam → Frame Capture (OpenCV) → Landmark Detection (MediaPipe Pose + Face Mesh) → Feature Extraction → Rule-Based Analysis → Flask Server → Web Dashboard


## Methodology

### 1. Landmark Detection

The system uses MediaPipe Pose and Face Mesh models to extract key body and facial landmarks from each video frame.

### 2. Feature Extraction

Relevant spatial relationships are computed, including:

* Head position relative to shoulders
* Eye openness
* Mouth movement
* Head orientation

### 3. Attention Scoring

A rule-based scoring system assigns penalties based on detected issues such as slouching, drowsiness, or distraction.

### 4. State Classification

Based on the computed score, the system classifies the user into one of the following states:

* **Focused**
* **Attentive**
* **Low Attention**
* **Distracted**
* **Critical**


## Features

* Real-time video processing
* Multi-modal analysis (posture + facial behavior)
* Attention score (0–100)
* Issue-specific feedback
* Dynamic cognitive state classification
* Web-based dashboard using Flask
* No dataset or training required


## Technologies Used

* Python
* OpenCV
* MediaPipe
* Flask
* HTML, CSS, JavaScript


## Output Demonstration

### Focused State

![Focused](outputs/focused.png)

### Distracted State

![Distracted](outputs/distracted.png)

### Low Attention State

![Low Attention](outputs/low_attention.png)


## Results

The system successfully performs real-time attention monitoring and provides interpretable feedback through a scoring mechanism and issue identification. It demonstrates the feasibility of lightweight computer vision solutions for behavioral analysis without reliance on large datasets.



## Limitations

* Rule-based system may not generalize to all environments
* Performance depends on lighting and camera quality
* Does not perform true emotion classification


## Future Scope

* Integration with deep learning-based emotion recognition
* Audio alert system for prolonged inattention
* Deployment as a web or mobile application
* Historical analytics and attention tracking

## Conclusion

This project demonstrates an effective approach to real-time attention monitoring using computer vision. By combining posture and facial analysis, it provides a scalable and practical solution for enhancing engagement in digital environments.



## Author

Pratyaksha Singh
