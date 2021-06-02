import cv2
import mediapipe as mp
import time

# Create video object to use web-cam no. 0 (diff no. for other web-cams)
cap = cv2.VideoCapture(0)

# Define pretrained hands object
mpHands = mp.solutions.hands
hands = mpHands.Hands()

# Draw points object
mpDraw = mp.solutions.drawing_utils


while True:
    success, img = cap.read()  # that will give us our frame

    # Load image to hands object
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    # Extract information from results object
    # print(results.multi_hand_landmarks)  # check if any object detected
    
    if results.multi_hand_landmarks:  # if detects look up object

        for handLms in results.multi_hand_landmarks:
            # Extract information for each hand and display handLms in original image -> img 
            mpDraw.draw_landmarks(img, handLms)

    cv2.imshow("Image", img)
    cv2.waitKey(1)