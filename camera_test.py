print("ZeroTouch program started!")

import cv2

camera = cv2.VideoCapture(0)

print("Camera opened:", camera.isOpened())

if not camera.isOpened():
    print("Unable to access webcam")
else:
    print("Webcam connected successfully!")

    while True:
        success, frame = camera.read()

        if not success:
            print("Camera frame could not be read")
            break

        cv2.imshow("ZeroTouch Camera", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    camera.release()
    cv2.destroyAllWindows()
