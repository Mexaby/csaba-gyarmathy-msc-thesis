import matplotlib.pyplot as plt
from contour_detection import find_contours
import cv2
from object_detection import load_object_detector, detect_objects, match_contours_to_objects, draw_object_labels_on_contours

def annotate_contours_with_objects(image, contours):
    """
    Detect objects and annotate contours with object labels.
    Returns the annotated image and the contour labels.
    """
    model = load_object_detector()
    objects = detect_objects(image, model)
    contour_labels = match_contours_to_objects(contours, objects)
    annotated_img = draw_object_labels_on_contours(image, contours, contour_labels)
    return annotated_img, contour_labels


def interactive_epsilon_adjustment(image, binary, initial_epsilon=2.0):
    """
    Interactive function to adjust the epsilon parameter for contour approximation.
    Args:
        image (np.ndarray): The original image on which contours are drawn.
        binary (np.ndarray): Binarized version of the image for contour detection.
        initial_epsilon (float): Starting value for epsilon in contour approximation.
        scale_factor (float): Factor by which the contour image is scaled.
    Returns:
        tuple: A tuple containing the contours and the final epsilon value.
    """
    epsilon = initial_epsilon
    fig, ax = plt.subplots()
    fig.canvas.manager.set_window_title('Contours Adjustment')
    plt.axis('off')

    contours = find_contours(binary, approx_epsilon=epsilon)
    contour_img = image.copy()
    cv2.drawContours(contour_img, contours, -1, (0, 255, 0), 2)
    im_plot = ax.imshow(cv2.cvtColor(contour_img, cv2.COLOR_BGR2RGB))
    title = ax.set_title(f"Epsilon: {epsilon:.2f}")

    def on_key(event):
        nonlocal epsilon, contours, contour_img
        if event.key == 'right':
            epsilon += 0.02
        elif event.key == 'left':
            epsilon = max(0.02, epsilon - 0.02)
        elif event.key == 'enter':
            plt.close()
            return
        elif event.key == 'escape':
            epsilon = None
            plt.close()
            return

        contours = find_contours(binary, approx_epsilon=epsilon)
        contour_img = image.copy()
        cv2.drawContours(contour_img, contours, -1, (0, 255, 0), 2)
        im_plot.set_data(cv2.cvtColor(contour_img, cv2.COLOR_BGR2RGB))
        title.set_text(f"Epsilon: {epsilon:.2f}")
        fig.canvas.draw_idle()

    fig.canvas.mpl_connect('key_press_event', on_key)
    plt.show()
    return contours, epsilon
