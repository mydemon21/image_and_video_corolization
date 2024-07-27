# Image/Video Colorization App

## Overview

This Python application allows you to colorize grayscale images and videos using a pre-trained deep learning model. The application provides a simple graphical user interface (GUI) for selecting images or videos, processing them to add color, and saving the results.

## Features

- **Colorize Images**: Convert grayscale images to color.
- **Colorize Videos**: Convert grayscale videos to color and save the result.
- **Save Results**: Save the colorized images and videos in appropriate formats.

## Requirements

- Python 3.x
- Libraries:
  - `numpy`
  - `opencv-python`
  - `Pillow`

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/mydemon21/image_and_video_corolization.git
    cd image_and_video_corolization
    ```

2. **Install dependencies**:

    Create a virtual environment (optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

    Install the required libraries:

    ```bash
    pip install -r requirements.txt
    ```

3. **Prepare the model files**:

    Ensure you have the following files in the `model` directory:

    - `colorization_deploy_v2.prototxt`
    - `pts_in_hull.npy`
    - `colorization_release_v2.caffemodel` (This file is not included in the repository. Download it from [this Dropbox link](https://www.dropbox.com/s/dx0qvhhp5hbcx7z/colorization_release_v2.caffemodel?dl=1) and place it in the `model` directory.)

## Model Description

The application uses a pre-trained deep learning model for colorizing grayscale images and videos. Here’s a brief overview of how the model works:

1. **Model Files**:
    - **`colorization_deploy_v2.prototxt`**: This is the network architecture configuration file in Caffe's prototxt format. It defines the layers and operations of the neural network.
    - **`colorization_release_v2.caffemodel`**: This file contains the pre-trained weights for the model, which were learned during the training phase. Download this file from [this Dropbox link](https://www.dropbox.com/s/dx0qvhhp5hbcx7z/colorization_release_v2.caffemodel?dl=1).
    - **`pts_in_hull.npy`**: This file contains the colorization points that help the model map grayscale images to their corresponding colors.

2. **Colorization Process**:
    - **Preprocessing**: The input grayscale image is scaled and converted to the LAB color space, which separates the lightness (L) from the color components (a and b).
    - **Model Input**: The L channel (lightness) is extracted and fed into the deep learning model. The model predicts the a and b color channels.
    - **Postprocessing**: The predicted a and b channels are combined with the original L channel to reconstruct the colorized image in the LAB color space. The LAB image is then converted back to the BGR color space for display and saving.

    The Caffe model is loaded using OpenCV’s DNN module, and the colorization layers are modified to apply the pre-trained weights. The model’s output is processed and resized to match the original image dimensions.

## Usage

1. **Run the application**:

    ```bash
    python main.py
    ```

2. **Using the application**:
   - Click the "Select Image/Video" button to choose an image or video file.
   - The application will display the original and colorized images/videos side by side.
   - Click "Save Image" to save the colorized image.
   - Click "Save Video (MP4)" to save the colorized video.

## Notes

- The model files must be in the correct directory (`model/`) for the application to work.
- Adjust the paths and settings in `main.py` as needed to match your environment.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
