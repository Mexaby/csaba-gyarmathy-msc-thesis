import cv2
import numpy as np


def approximate_contours(contours, epsilon=0.1):
    """
    Approximate contours to polygons using the Ramer–Douglas–Peucker algorithm.
    Args:
        contours (list): List of contours, each as a numpy array of (x, y) points.
        epsilon (float): Approximation accuracy. Higher values result in fewer points.
    Returns:
        list: List of approximated contours.
    """
    approx_contours = []
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, epsilon, closed=True)
        approx_contours.append(approx)
    return approx_contours


def find_contours(image, min_area=100, ignore_border=True, approx_epsilon=0.1):
    """
    Detect contours in a binarized image using OpenCV, filtering out the outer border and small areas.
    Optionally approximate contours to polygons.
    Args:
        image (np.ndarray): Binarized (single-channel) image.
        min_area (int): Minimum area for a contour to be considered valid.
        ignore_border (bool): Whether to ignore contours touching the image border.
        approx_epsilon (float): Approximation accuracy for polygons.
    Returns:
        list: List of filtered and approximated contours, each contour is a numpy array of (x, y) points.
    """
    height, width = image.shape[:2]
    contours, _ = cv2.findContours(
        image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    filtered = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < min_area:
            continue
        if ignore_border:
            x, y, w, h = cv2.boundingRect(cnt)
            if x <= 1 or y <= 1 or x + w >= width - 1 or y + h >= height - 1:
                continue
        filtered.append(cnt)

    if approx_epsilon > 0:
        filtered = approximate_contours(filtered, epsilon=approx_epsilon)
    return filtered
