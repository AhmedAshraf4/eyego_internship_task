# Real-Time Object Tracking

This repository contains two Python implementations for real-time single-object tracking using a webcam feed.





## Project Overview

This task implements a real-time object tracker that can follow a specific object in a live webcam feed.

The system supports two modes:

1. **Manual ROI selection** in `main.py`  
   The user selects the object in the first frame using a bounding box.

2. **Gesture-based ROI selection** in `hand_select.py`  
   The user shows an open palm to arm selection mode, then uses a pinch gesture to draw the bounding box with the hand.

After selection, both versions use the **OpenCV CSRT tracker** to follow the selected object in real time.

---

## Implementation Details

### 1. `main.py`
This is the basic version of the tracker.

#### Flow
- Open the webcam using OpenCV
- Read a few initial frames to warm up the camera
- Display the first frame and let the user select a bounding box using `cv2.selectROI`
- Initialize the **CSRT** tracker with the selected region
- In each new frame:
  - read the frame from the webcam
  - update the tracker
  - draw the predicted bounding box if tracking succeeds
  - show a lost message if tracking fails

#### Why CSRT?
CSRT (**Discriminative Correlation Filter with Channel and Spatial Reliability**) is a classical OpenCV tracking algorithm. It is well-suited for this task because it is generally more stable and accurate than lighter trackers for single-object tracking.

---

### 2. `hand_select.py`
This is the gesture-controlled version.

#### Flow
- Open the webcam
- Use **MediaPipe Hands** to detect hand landmarks in real time
- Detect an **open palm** to arm the system
- Detect a **pinch gesture** using the thumb and index fingertip distance
- While pinching, update the second corner of the bounding box using the index finger position
- When the pinch is released:
  - finalize the bounding box
  - initialize the CSRT tracker
- Continue tracking the selected object without requiring the hand to remain visible

#### Gesture Logic
- **Open palm** → enables selection mode
- **Pinch** → starts drawing the bounding box
- **Release pinch** → confirms selection and starts tracking

This version improves the interaction by removing the need for mouse-based ROI selection.

---

## Repository Structure

```bash
├── main.py
├── hand_select.py
├── requirements.txt
└── README.md
```

---

## Requirements

- Python 3.10 or 3.11
- Webcam access
- The following Python libraries:
  - `opencv-contrib-python`
  - `mediapipe`

---

## Installation / Deployment Instructions

### 1. Clone the repository
```bash
git clone https://github.com/AhmedAshraf4/eyego_internship_task
cd eyego_internship_task
```

### 2. Create a virtual environment

#### Windows
```bash
python -m venv .venv
.venv\Scripts\activate
```

#### Linux / macOS
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## How to Run

### Run the basic tracker
```bash
python main.py
```

### Run the hand gesture tracker
```bash
python hand_select.py
```

---

## Controls

### `main.py`
- Draw a bounding box around the object and press **Enter**
- Press `q` to quit
- Press `r` to reselect another object

### `hand_select.py`
- Show an **open palm** to arm selection mode
- Use a **pinch gesture** to draw the bounding box
- Release the pinch to confirm selection
- Press `q` to quit
- Press `r` to reset and select again

---

## Notes

- Make sure no other application is using the webcam
- Good lighting improves hand detection performance in `hand_select.py`
- If MediaPipe causes issues, use Python 3.10 or 3.11
- CSRT is more accurate than some lighter trackers, but may run slightly slower



