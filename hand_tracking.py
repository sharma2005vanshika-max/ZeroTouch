import cv2
import mediapipe as mp

print("ZeroTouch: Hand Tracking Started!")

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Unable to access webcam!")
    hands.close()
    raise SystemExit

print("Camera connected! Show your hand.")

while True:
    success, frame = camera.read()
    if not success:
        print("Unable to read camera frame.")
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
            )
        cv2.putText(
            frame, "Hand Detected!", (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2
        )

    cv2.imshow("ZeroTouch - Hand Tracking", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

camera.release()
hands.close()
cv2.destroyAllWindows()
