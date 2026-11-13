ZeroTouch 🖐️

Touchless Gesture-Controlled Desktop Interface

ZeroTouch is a Python-based project that allows users to interact with their computer using hand gestures instead of a traditional mouse.

It uses computer vision and hand tracking to detect hand movements and translate them into mouse actions.

✨ Features

- Real-time hand detection and tracking
- Control mouse cursor using your index finger
- Perform clicks using a thumb-index finger pinch gesture
- Webcam-based gesture recognition
- Touch-free computer interaction

🛠️ Technologies Used

- Python
- OpenCV
- MediaPipe
- NumPy
- PyAutoGUI

📁 Project Structure

- "camera_test.py" – Tests webcam access
- "hand_tracking.py" – Detects and tracks hand landmarks
- "gesture_recognition.py" – Recognizes hand gestures
- "virtual_mouse.py" – Controls the mouse using hand movements

🚀 Getting Started

1. Clone the repository

git clone YOUR_GITHUB_REPOSITORY_URL

2. Open the project folder

cd ZeroTouch

3. Create a virtual environment

python3 -m venv .venv

4. Activate the environment

source .venv/bin/activate

5. Install dependencies

pip install opencv-python==4.10.0.84 mediapipe==0.10.21 numpy==1.26.4 pyautogui

6. Run ZeroTouch

python virtual_mouse.py

🔐 Permissions

On macOS, allow camera access for your terminal or application. You may also need to enable Accessibility permission for mouse control.

🎯 Project Goal

To explore human-computer interaction through computer vision and make desktop interaction more intuitive, accessible, and touchless.

👩‍💻 Developer

Vanshika Sharma

---

ZeroTouch — Interact with your computer, without touching it.