import cv2
import time
import mediapipe as mp
import math


def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def finger_is_up(lm, tip_id, pip_id):
    return lm[tip_id].y < lm[pip_id].y


cap = cv2.VideoCapture(0)


for _ in range(10):
    cap.read()
    time.sleep(0.01)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    model_complexity=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

no_select = False
curr_slect = False
roi_start = None
roi_end = None
tracker = None
tracking_on = False

prev_time = time.time()

while True:
    ok, frame = cap.read()
    if not ok or frame is None:
        break

    frame = cv2.flip(frame, 1)
    h, w = frame.shape[:2]

    if tracking_on:
        status_text = "Tracking"
        status_color = (0, 255, 0)
    else:
        status_text = "Show an open palm to start selecting"
        status_color = (0, 0, 0)

    if not tracking_on:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        res = hands.process(rgb)

        if res.multi_hand_landmarks:
            hand = res.multi_hand_landmarks[0]
            lm = hand.landmark

            thumb_tip = (int(lm[4].x * w), int(lm[4].y * h))
            index_tip = (int(lm[8].x * w), int(lm[8].y * h))

            index_up  = finger_is_up(lm, 8, 6)
            middle_up = finger_is_up(lm, 12, 10)
            ring_up   = finger_is_up(lm, 16, 14)
            pinky_up  = finger_is_up(lm, 20, 18)

            open_palm = index_up and middle_up and ring_up and pinky_up
            pinch = dist(thumb_tip, index_tip) < 50

            if open_palm:
                no_select = True
                status_text = "pinch (thumb+index) to start drawing bounding box"
                status_color = (0, 0, 0)
            else:
                if not curr_slect:
                    no_select = False

            if no_select and pinch and not curr_slect:
                curr_slect = True
                roi_start = index_tip
                roi_end = index_tip

            if curr_slect:
                roi_end = index_tip
                status_text = "Drawing bounding box ... release pinch to confirm"
                status_color = (0, 0, 0)

                x1, y1 = roi_start
                x2, y2 = roi_end
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 2)

                if not pinch:
                    curr_slect = False
                    no_select = False

                    x1, y1 = roi_start
                    x2, y2 = roi_end
                    x, y = min(x1, x2), min(y1, y2)
                    ww, hh = abs(x2 - x1), abs(y2 - y1)

                    roi = (x, y, ww, hh)
                    tracker = cv2.TrackerCSRT_create()
                    tracker.init(frame, roi)
                    tracking_on = True
                    status_text = "Tracking"
                    status_color = (0, 255, 0)


            cv2.circle(frame, index_tip, 6, (255, 255, 255), -1)
            cv2.circle(frame, thumb_tip, 6, (200, 200, 200), -1)

    if tracking_on and tracker is not None:
        success, box = tracker.update(frame)
        if success:
            x, y, ww, hh = [int(v) for v in box]
            cv2.rectangle(frame, (x, y), (x + ww, y + hh), (0, 255, 0), 2)
            status_text = "Tracking"
            status_color = (0, 255, 0)
        else:
            status_text = "Tracking Lost"
            status_color = (0, 0, 255)


    cv2.putText(frame, status_text, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)
    cv2.putText(frame, "q quit or r reselect", (10, frame.shape[0] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 2)

    cv2.imshow("Tracker", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    if key == ord("r"):
        tracking_on = False
        tracker = None
        no_select = False
        curr_slect = False
        roi_start = None
        roi_end = None


cap.release()
cv2.destroyAllWindows()
hands.close()
