import cv2
import mediapipe as mp
import pyautogui as auto

camera = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.2, min_tracking_confidence=0.3)


while True:
    _,frame = camera.read()
    frame = cv2.flip(frame, 1)

    results = hands.process(frame)

    rectangle_width = 480
    rectangle_height = 360


    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for landmark in hand_landmarks.landmark[8:9]:
                x = int(landmark.x * frame.shape[1])
                y = int(landmark.y * frame.shape[0])
                print(x,y)
                #frame is 640:480(4:3) use 600:450 then map that to the screens resolution
                transformedX = (x/rectangle_width)*1920
                transformedY = (y/rectangle_height)*1080
                auto.moveTo(transformedX,transformedY)
                cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

    # Draw the rectangle on the frame
    cv2.rectangle(frame, (0, 0), (rectangle_width, rectangle_height), (255, 0, 0), 2)

    cv2.imshow("Camera", frame)

    if (cv2.waitKey(1) == ord("q")):
        break

camera.release()
cv2.destroyWindow()