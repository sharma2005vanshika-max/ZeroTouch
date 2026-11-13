import cv2
import mediapipe as mp
import math

print("ZeroTouch: Gesture Recognition Started!")

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

camera = cv2.VideoCapture(0)

def distance(point1, point2):
    return math.sqrt(
        (point1.x - point2.x) ** 2 +
        (point1.y - point2.y) ** 2
    )

def recognize_gesture(hand):
    thumb_tip = hand.landmark[4]
    index_tip = hand.landmark[8]

    index_up = hand.landmark[8].y < hand.landmark[6].y
    middle_up = hand.landmark[12].y < hand.landmark[10].y
    ring_up = hand.landmark[16].y < hand.landmark[14].y
    pinky_up = hand.landmark[20].y < hand.landmark[18].y

    pinch_distance = distance(thumb_tip, index_tip)

    if pinch_distance < 0.05:
        return "PINCH"

    if index_up and not middle_up and not ring_up and not pinky_up:
        return "POINTING"

    if index_up and middle_up and ring_up and pinky_up:
        return "OPEN PALM"

    if not index_up and not middle_up and not ring_up and not pinky_up:
        return "FIST"

    return "UNKNOWN"


if not camera.isOpened():
    print("Unable to access webcam!")
    hands.close()
    raise SystemExit

print("Camera connected! Try different hand gestures.")

while True:
    success, frame = camera.read()

    if not success:
        print("Unable to read camera frame.")
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_frame)

    gesture = "NO HAND DETECTED"

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            gesture = recognize_gesture(hand_landmarks)

    cv2.putText(
        frame,
        "Gesture: " + gesture,
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (0, 255, 0),
        2
    )

    cv2.imshow("ZeroTouch - Gesture Recognition", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

camera.release()
hands.close()
cv2.destroyAllWindows()
