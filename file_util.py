import cv2
import numpy as np
import os
from PyQt5.QtWidgets import QApplication, QFileDialog
import sys


def load_image(path):
    """
    Load an image from the specified file path.
    Args:
        path (str): Path to the image file.
    Returns:
        np.ndarray: Loaded image in BGR format.
    """
    return cv2.imread(path)


def binarize_image(image, threshold=127):
    """
    Convert an image to grayscale and binarize it using a fixed threshold.
    Args:
        image (np.ndarray): Input image (BGR or grayscale).
        threshold (int): Threshold value for binarization.
    Returns:
        np.ndarray: Binarized (single-channel) image.
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    return binary


def save_gcode_to_file(gcode_str, file_path):
    """
    Save the G-code string to a file, ensuring it has a .gcode extension.
    Args:
        gcode_str (str): The G-code content to save.
        file_path (str): The desired file path (will enforce .gcode extension).
    """
    base, ext = os.path.splitext(file_path)
    if ext.lower() != ".gcode":
        file_path = base + ".gcode"
    with open(file_path, "w") as f:
        f.write(gcode_str)


def select_image_file():
    """
    Open a file dialog to select an image file using PyQt5.
    Returns:
        str: Path to the selected image file, or None if canceled.
    """
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
        created_app = True
    else:
        created_app = False
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    file_path, _ = QFileDialog.getOpenFileName(
        None,
        "Select Image File",
        "",
        "Image files (*.jpg *.jpeg *.png *.bmp);;All files (*.*)",
        options=options
    )
    if created_app:
        app.exit()
    return file_path if file_path else None


def select_save_file():
    """
    Open a file dialog to select a save location for G-code file using PyQt5.
    Returns:
        str: Path to save the G-code file, or None if canceled.
    """
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
        created_app = True
    else:
        created_app = False
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    file_path, _ = QFileDialog.getSaveFileName(
        None,
        "Save G-code File",
        "",
        "G-code files (*.gcode);;All files (*.*)",
        options=options
    )
    if created_app:
        app.exit()
    return file_path if file_path else None


def get_image_info(image):
    """
    Get information about an image.
    Args:
        image (np.ndarray): The image to get information about.
    Returns:
        dict: Dictionary containing image information (height, width, channels).
    """
    if image is None:
        return None

    height, width = image.shape[:2]
    channels = 1 if len(image.shape) == 2 else image.shape[2]

    return {
        "height": height,
        "width": width,
        "channels": channels,
        "resolution": f"{width}x{height}"
    }
