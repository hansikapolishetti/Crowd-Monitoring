import cv2
from ultralytics import YOLO
import supervision as sv
from collections import deque

# Use a stronger model for better human detection
model = YOLO("yolov8m.pt")

tracker = sv.ByteTrack()

box_annotator = sv.BoxAnnotator()
label_annotator = sv.LabelAnnotator()

cap = cv2.VideoCapture(0)

# history for stable count
count_history = deque(maxlen=10)

while True:

    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLO
    results = model(frame, verbose=False)[0]

    detections = sv.Detections.from_ultralytics(results)

    # Keep only humans
    detections = detections[detections.class_id == 0]

    # Allow partial humans
    if detections.confidence is not None:
        detections = detections[detections.confidence > 0.35]

    # Tracking
    detections = tracker.update_with_detections(detections)

    people_count = len(detections)

    # smooth count
    count_history.append(people_count)
    stable_count = max(count_history)

    labels = [f"Person #{id}" for id in detections.tracker_id]

    frame = box_annotator.annotate(frame, detections)
    frame = label_annotator.annotate(frame, detections, labels)

    # Density logic
    if stable_count <= 1:
        density = "LOW"
        color = (0,255,0)
    elif stable_count <= 2:
        density = "MEDIUM"
        color = (0,255,255)
    else:
        density = "HIGH"
        color = (0,0,255)

    cv2.putText(frame, f"People Count: {stable_count}", (20,40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    cv2.putText(frame, f"Crowd Density: {density}", (20,80),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    cv2.imshow("AI Crowd Monitoring", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
