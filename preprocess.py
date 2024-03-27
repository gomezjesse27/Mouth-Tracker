"""
Created 3/27/2024
Preprocessing Module for CBMT Project

This module contains functions for loading, preprocessing, and augmenting
the image data for the Calibration-Based Mouth Tracker (CBMT) project. It
includes functionalities for resizing images, converting them to grayscale,
normalizing pixel values, and splitting the dataset into training, validation,
and test sets.

Proposed Functions:
- load_data: Load the image dataset from a specified directory.
- preprocess_image: Apply preprocessing steps to a single image.
- split_data: Split the dataset into training, validation, and test sets.
- augment_data: Apply data augmentation techniques to the training set (optional).

"""
