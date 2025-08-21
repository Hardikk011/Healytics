# Models Directory

This directory should contain your machine learning model file.

## Required File
- `skin_disease_model_best.h5` - Your trained skin disease classification model

## Instructions
1. Place your `skin_disease_model_best.h5` file in this directory
2. The model should be compatible with TensorFlow/Keras
3. The model should expect input images of size 224x224 pixels
4. The model should output predictions for 7 classes:
   - 0: melanoma
   - 1: basal_cell_carcinoma
   - 2: squamous_cell_carcinoma
   - 3: benign
   - 4: actinic_keratosis
   - 5: dermatofibroma
   - 6: vascular_lesion

## Model Requirements
- Input shape: (224, 224, 3) - RGB images
- Output: 7-class classification probabilities
- Format: HDF5 (.h5) file
- Framework: TensorFlow/Keras

## Testing
After placing the model file, you can test it by running the Django server and making a prediction through the web interface.
