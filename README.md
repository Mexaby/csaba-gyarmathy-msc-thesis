# Master's Thesis

## Artificial Intelligence in CNC Applications: Enhancing Object Contour Detection and G-Code Generation Compared to Traditional Methods

---

### Abstract

This thesis aims to explore and compare traditional image processing and computer vision (IPCV) techniques with modern AI/ML-based methods for object contour extraction and G-code generation. The goal is to evaluate the strengths and limitations of both approaches and identify how AI can enhance the automation pipeline for CNC-related tasks. The project is based on my bachelor's thesis.

---

### 📋 What's Been Done

- ✅ Rewritten all logic and code in Python
- ✅ Integrated **working** contour segmentation with interactive parameter tuning
- ❌ Cross-platform support removed
- ❌ CNC hardware support removed
- ✅ Tested object detection using pretrained YOLOv5 models
- ✅ Attempted fine-tuning of detection models

---

### 🔧 TODO

- 🔍 Find or create a suitable dataset for the AI/ML pipeline:
  - 📁 Collect a dataset of real or synthetic images
  - 🖤 Convert to binary counterparts
  - ✒️ Generate contour-only images
  - 🛠️ Use existing or custom software to produce G-code for each image
  - 📦 Final dataset should include:
    - Original image
    - Binary image
    - Contour-only image
    - G-code file

- 🧠 Train a model to predict the G-code representation of an image  
- 📊 Compare the model’s output with G-code from traditional IPCV methods  
- 🖼️ Develop a user interface for demonstration and testing

---

