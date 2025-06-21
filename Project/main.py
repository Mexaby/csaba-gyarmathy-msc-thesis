import os
import cv2
import datetime
from file_util import *
from contour_detection import find_contours
from g_code_generation import contours_to_gcode
from window_util import interactive_epsilon_adjustment, annotate_contours_with_objects


def display_menu(image_loaded=False):
    """
    Display the main menu and return the user's choice.
    Args:
        image_loaded (bool): Indicates if an image is loaded.
    Returns:
        str: User's choice as a string.
    """
    print("\n===== Image to G-code Converter for CNC Machines =====\n")
    print("1. Load Image")

    if image_loaded:
        print("2. Generate G-code")

    print("3. Exit")

    return input(f"\nEnter your choice: ")


def display_image(image, window_name="Image Preview"):
    """
    Display an image in a window with proper scaling.
    Args:
        image (np.ndarray): The image to display.
        window_name (str): The name of the window.
    Returns:
        None
    """
    if image is None:
        return

    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    screen_width = 1280
    screen_height = 720

    height, width = image.shape[:2]
    scale_width = screen_width / width * 0.8
    scale_height = screen_height / height * 0.8
    scale = min(scale_width, scale_height)

    new_width = int(width * scale)
    new_height = int(height * scale)
    cv2.resizeWindow(window_name, new_width, new_height)

    cv2.imshow(window_name, image)
    cv2.waitKey(0)
    cv2.destroyWindow(window_name)


def main():
    input_path = None
    threshold = 200
    feed_rate = 3500.0
    pen_down = 30
    pen_up = 50
    wait_ms = 150

    image = None
    binary = None
    contours = None
    gcode = None

    while True:
        choice = display_menu(image_loaded=(image is not None))

        if choice == '1':
            input_path = select_image_file()
            if input_path:
                print(f"\nSelected image: {os.path.basename(input_path)}")
                image = load_image(input_path)
                if image is not None:
                    info = get_image_info(image)
                    print(f"Image loaded successfully!")
                    print(f"Resolution: {info['resolution']}")
                    print(f"Channels: {info['channels']}")

                    display_image(image, "Input Image")

                    print("\nBinarizing image with default threshold...")
                    binary = binarize_image(image, threshold=threshold)
                    display_image(binary, "Binarized Image")
                    print(f"Image binarized with threshold: {threshold}")

                    # Interactive epsilon adjustment for contours
                    print(
                        "\nAdjust contour simplification (epsilon) interactively. Use left/right arrows to change, Enter to confirm.")
                    contours, epsilon = interactive_epsilon_adjustment(
                        image, binary, initial_epsilon=2.0)
                    if contours is not None:
                        print(
                            f"Contours adjusted. Selected epsilon: {epsilon}")
                        # Annotate contours with object detection labels
                        annotated_img, contour_labels = annotate_contours_with_objects(image, contours)
                        display_image(annotated_img, "Contours + Object Labels")
                    else:
                        print(
                            "Contour adjustment canceled. You can reload the image to try again.")
                        image = None
                        binary = None
                        contours = None
            else:
                print("No image selected.")

        elif choice == '2' and image is not None:
            print("Detecting contours...")
            # Use contours from epsilon adjustment if available
            if contours is None:
                contours = find_contours(binary)
            if not contours:
                print("No contours found in the image.")
                continue
            print(f"Found {len(contours)} contour(s).")

            contour_img = image.copy()
            cv2.drawContours(contour_img, contours, -1, (0, 255, 0), 2)
            display_image(contour_img, "Contours Image")

            print("Generating G-code...")
            gcode = contours_to_gcode(
                contours, feed_rate=feed_rate, pen_down=pen_down, pen_up=pen_up, wait_ms=wait_ms)

            output_dir = os.path.join(os.path.dirname(__file__), "output")
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"gcode_{timestamp}.gcode"
            output_path = os.path.join(output_dir, output_filename)
            save_gcode_to_file(gcode, output_path)
            print(f"G-code successfully written to: {output_path}")

        elif choice == '3':
            # Exit
            print("Exiting program. Goodbye!")
            break

        else:
            max_choice = 3 if image is not None else 2
            print(
                f"Invalid choice. Please enter a number between 1 and {max_choice}.")

        print("\nPress Enter to continue...")
        input()


if __name__ == "__main__":
    main()
