import cv2
import mediapipe as mp
import pyautogui
import math

print("ZeroTouch: Virtual Mouse Started!")

# --------------------------------
# 1. INITIALISE MEDIAPIPE
# --------------------------------

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# --------------------------------
# 2. GET SCREEN DIMENSIONS
# --------------------------------

screen_width, screen_height = pyautogui.size()

print("Screen size:", screen_width, screen_height)

# --------------------------------
# 3. OPEN WEBCAM
# --------------------------------

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Unable to access webcam!")
    hands.close()
    raise SystemExit

print("Camera connected!")
print("Move index finger to control cursor.")
print("Pinch thumb and index finger to click.")
print("Press ESC to exit.")

# --------------------------------
# 4. CURSOR SETTINGS
# --------------------------------

smooth_x = 0
smooth_y = 0

smoothing = 0.5

click_threshold = 0.04
pinch_was_active = False

# --------------------------------
# 5. DISTANCE FUNCTION
# --------------------------------

def distance(point1, point2):
    return math.sqrt(
        (point1.x - point2.x) ** 2 +
        (point1.y - point2.y) ** 2
    )

# --------------------------------
# 6. MAIN PROGRAM LOOP
# --------------------------------

try:
    while True:

        success, frame = camera.read()

        if not success:
            print("Unable to read camera frame!")
            break

        # Mirror webcam image
        frame = cv2.flip(frame, 1)

        # Convert BGR image to RGB
        rgb_frame = cv2.cvtColor(
            frame, cv2.COLOR_BGR2RGB
        )

        # Detect hand
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:

            for hand_landmarks in results.multi_hand_landmarks:

                # Get index fingertip
                index_finger = hand_landmarks.landmark[8]

                # Get thumb fingertip
                thumb_tip = hand_landmarks.landmark[4]

                # --------------------------------
                # 7. CURSOR MOVEMENT
                # --------------------------------

                target_x = int(
                    index_finger.x * screen_width
                )

                target_y = int(
                    index_finger.y * screen_height
                )

                # Smooth cursor movement
                smooth_x = smooth_x + (
                    target_x - smooth_x
                ) * smoothing

                smooth_y = smooth_y + (
                    target_y - smooth_y
                ) * smoothing

                # Move mouse cursor
                pyautogui.moveTo(
                    int(smooth_x),
                    int(smooth_y)
                )

                # --------------------------------
                # 8. PINCH-TO-CLICK
                # --------------------------------

                pinch_distance = distance(
                    thumb_tip,
                    index_finger
                )

                pinch_active = (
                    pinch_distance < click_threshold
                )

                # Click only when pinch starts
                if pinch_active and not pinch_was_active:

                    pyautogui.click()

                    print("Mouse clicked!")

                # Remember current pinch state
                pinch_was_active = pinch_active

                # --------------------------------
                # 9. DISPLAY HAND LANDMARKS
                # --------------------------------

                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS
                )

                cv2.putText(
                    frame,
                    "ZeroTouch: Virtual Mouse Active",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2
                )

                gesture_text = (
                    "PINCH - CLICK"
                    if pinch_active
                    else "MOVE CURSOR"
                )

                cv2.putText(
                    frame,
                    gesture_text,
                    (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 255),
                    2
                )

        else:
            # Reset pinch state when hand disappears
            pinch_was_active = False

        # Show webcam window
        cv2.imshow(
            "ZeroTouch - Virtual Mouse",
            frame
        )

        # ESC key exits the program
        if cv2.waitKey(1) & 0xFF == 27:
            break

finally:

    # --------------------------------
    # 10. CLEANUP
    # --------------------------------

    camera.release()
    hands.close()
    cv2.destroyAllWindows()

    print("ZeroTouch Virtual Mouse Stopped!")