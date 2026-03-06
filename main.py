import cv2
import time

cap = cv2.VideoCapture(0)

first_frame = None
for _ in range(25):
    ok, frame = cap.read()
    if ok and frame is not None:
        first_frame = frame
    time.sleep(0.01)

#mirror video
first_frame = cv2.flip(first_frame, 1)

overlay = first_frame.copy()
cv2.putText(
    overlay,
    "Draw a box around the object, then press ENTER",
    (10, 30),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.7,
    (255, 255, 255),
    2
)

roi = cv2.selectROI("Select Object", overlay, fromCenter=False, showCrosshair=True)
cv2.destroyWindow("Select Object")

x, y, w, h = roi


tracker = cv2.TrackerCSRT_create()
tracker.init(first_frame, roi)

prev_time = time.time()

while True:
    ok, frame = cap.read()
    if not ok or frame is None:
        print("Frame read failure")
        break

    frame = cv2.flip(frame, 1)

    success, box = tracker.update(frame)


    if success:
        x, y, w, h = [int(v) for v in box]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, "Tracking", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    else:
        cv2.putText(frame, "Tracking Lost", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.putText(frame, "q quit or r reselect", (10, frame.shape[0] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 2)

    cv2.imshow("Tracker", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

    if key == ord("r"):
        roi = cv2.selectROI("Select Object", frame, fromCenter=False, showCrosshair=True)
        cv2.destroyWindow("Select Object")
        x, y, w, h = roi
        if w > 0 and h > 0:
            tracker = cv2.TrackerCSRT_create()
            tracker.init(frame, roi)

cap.release()
cv2.destroyAllWindows()