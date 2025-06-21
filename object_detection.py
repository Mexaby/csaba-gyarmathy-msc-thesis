import cv2
import numpy as np
from ultralytics import YOLO

#YOLOv5 models
YOLO_MODEL_NAMES = {
    "nano": "yolov5n.pt",      # Smallest and fastest model
    "small": "yolov5s.pt",     # Good balance of speed and accuracy
    "medium": "yolov5m.pt",    # Better accuracy, slower than small
    "large": "yolov5l.pt",     # High accuracy, slower
    "xlarge": "yolov5xu.pt"     # Highest accuracy, slowest
}

# Default model selection
YOLO_MODEL_NAME = YOLO_MODEL_NAMES["xlarge"]

def load_object_detector():
    """
    Loads the YOLOv5 model using the ultralytics package.
    Returns the loaded model.
    """
    model = YOLO(YOLO_MODEL_NAME)
    return model

def detect_objects(image, model, conf_threshold=0.5):
    """
    Detect objects in the image using YOLOv5.
    Returns a list of dicts: {class_id, label, confidence, box}
    """
    # YOLO expects RGB images
    rgb_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = model(rgb_img)
    objects = []
    for result in results:
        boxes = result.boxes.xyxy.cpu().numpy()  # (N, 4)
        classes = result.boxes.cls.cpu().numpy()  # (N,)
        confs = result.boxes.conf.cpu().numpy()   # (N,)
        for i in range(len(boxes)):
            if confs[i] >= conf_threshold:
                x1, y1, x2, y2 = boxes[i]
                class_id = int(classes[i])
                label = model.names[class_id] if hasattr(model, "names") else str(class_id)
                objects.append({
                    "class_id": class_id,
                    "label": label,
                    "confidence": float(confs[i]),
                    "box": (int(x1), int(y1), int(x2), int(y2))
                })
    return objects

def match_contours_to_objects(contours, objects):
    """
    For each contour, find the object detection box it overlaps with most.
    Returns a list of (label, confidence) for each contour (or None if no match).
    """
    contour_labels = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        best_iou = 0
        best_label = None
        best_conf = 0
        for obj in objects:
            ox1, oy1, ox2, oy2 = obj["box"]
            # Compute intersection-over-union (IoU)
            ix1 = max(x, ox1)
            iy1 = max(y, oy1)
            ix2 = min(x + w, ox2)
            iy2 = min(y + h, oy2)
            iw = max(0, ix2 - ix1)
            ih = max(0, iy2 - iy1)
            inter = iw * ih
            area_cnt = w * h
            area_obj = (ox2 - ox1) * (oy2 - oy1)
            union = area_cnt + area_obj - inter
            iou = inter / union if union > 0 else 0
            if iou > best_iou and iou > 0.2:  # Only consider significant overlap
                best_iou = iou
                best_label = obj["label"]
                best_conf = obj["confidence"]
        if best_label:
            contour_labels.append((best_label, best_conf))
        else:
            contour_labels.append(None)
    return contour_labels

def draw_object_labels_on_contours(image, contours, contour_labels):
    """
    Draws contours and their detected object labels on the image.
    """
    annotated = image.copy()
    for i, cnt in enumerate(contours):
        color = (0, 255, 0)
        cv2.drawContours(annotated, [cnt], -1, color, 2)
        if contour_labels[i]:
            label, conf = contour_labels[i]
            x, y, w, h = cv2.boundingRect(cnt)
            text = f"{label} ({conf:.2f})"
            cv2.putText(annotated, text, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    return annotated

