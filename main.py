import cv2
import mediapipe as mp
import pyautogui as auto
import pickle
import numpy as np
import AppOpener
import time

camera = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,max_num_hands=1,min_tracking_confidence=0.5,min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

camera = cv2.VideoCapture(0)

model = pickle.load(open("model.p","rb"))["model"]


lastOutput = ""
lastPerformed = ""
startTime = time.time()
threstholdTime = 1


while True:
    temp = []
    _, frame = camera.read()
    frame = cv2.flip(frame, 1)
    result = hands.process(frame)
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
            #                           mp_drawing_styles.get_default_hand_landmarks_style(),
            #                           mp_drawing_styles.get_default_hand_connections_style())
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                temp.append(x)
                temp.append(y)
        output = model.predict([np.asarray(temp)])

        if (lastOutput != output):
            lastOutput = output
            startTime = time.time()

        if (time.time() - startTime > threstholdTime and lastPerformed != output):
            lastPerformed = output
            startTime = time.time()
            print(output)
            if (output == "click"):
                auto.click()
            elif (output == "chrome"):
                AppOpener.open("chrome", match_closest=True)
            elif (output == "track"):
                auto.mouseUp()

    rectangle_width = 480
    rectangle_height = 360

    #print(results)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            #print(hand_landmarks)
            for landmark in hand_landmarks.landmark[8:9]:
                x = int(landmark.x * frame.shape[1])
                y = int(landmark.y * frame.shape[0])
                #print(x,y)
                #frame is 640:480(4:3) use 600:450 then map that to the screens resolution
                transformedX = (x/rectangle_width)*1920
                transformedY = (y/rectangle_height)*1080
                auto.moveTo(transformedX,transformedY)
                cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)


    #Draw the rectangle on the frame
    cv2.rectangle(frame, (0, 0), (rectangle_width, rectangle_height), (255, 0, 0), 2)

    cv2.imshow("Camera", frame)

    if (cv2.waitKey(1) == ord("q")):
        break

camera.release()
cv2.destroyWindow()
