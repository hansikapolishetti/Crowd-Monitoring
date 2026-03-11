
import cv2
from ultralytics import YOLO
import supervision as sv
from collections import deque

# Load strongest model
model = YOLO("yolov8x.pt")

tracker = sv.ByteTrack()

box_annotator = sv.BoxAnnotator()
label_annotator = sv.LabelAnnotator()

# Load video
cap = cv2.VideoCapture("crowd_video.mp4")

count_history = deque(maxlen=20)

while True:

    ret, frame = cap.read()

    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    # Upscale frame for better distant detection
    frame = cv2.resize(frame, None, fx=1.5, fy=1.5)

    # Run YOLO with large image size
    results = model(frame, conf=0.15, imgsz=1280, verbose=False)[0]

    detections = sv.Detections.from_ultralytics(results)

    # Keep only person class
    if len(detections) > 0:
        detections = detections[detections.class_id == 0]

    # Tracking
    detections = tracker.update_with_detections(detections)

    people_count = len(detections)

    count_history.append(people_count)
    stable_count = max(count_history)

    labels = [f"Person {i}" for i in detections.tracker_id]

    frame = box_annotator.annotate(frame, detections)
    frame = label_annotator.annotate(frame, detections, labels)

    # Density logic
    if stable_count <= 2:
        density = "LOW"
        color = (0,255,0)
    elif stable_count <= 5:
        density = "MEDIUM"
        color = (0,255,255)
    else:
        density = "HIGH"
        color = (0,0,255)

    cv2.putText(frame, "AI Crowd Monitoring System", (20,130),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

    cv2.putText(frame, f"People Count: {stable_count}", (20,50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    cv2.putText(frame, f"Crowd Density: {density}", (20,90),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    cv2.imshow("Crowd Monitoring", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()