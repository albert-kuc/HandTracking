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

# 
pTime = 0  # previous Time
cTime = 0  # current Time

while True:
    success, img = cap.read()  # that will give us our frame

    # Load image to hands object
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    # Extract information from results object
    # print(results.multi_hand_landmarks)  # check if any object detected
    
    if results.multi_hand_landmarks:  # if detects look up object

        for handLms in results.multi_hand_landmarks:

            # Extract information for each hand 

            # Get id number and ladnmark coordinates
            for id, lm in enumerate(handLms.landmark):
                # lm values are decimal places which is ratio of an image and not pixels
                # we need to multiply it with h, w of the image to get the pixel value
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                print(id, cx, cy)

            # Display handLms in original image -> img 
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
    
    # calculate frame rate
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    # include frame rate in img
    cv2.putText(img, str(int(fps)), (10, 70),  # display in img, fps to int, at position,  
                cv2.FONT_HERSHEY_PLAIN, 3,     # define font, define scale,
                (255, 0, 255), 3)               # define color (purple), define thickness

    cv2.imshow("Image", img)
    cv2.waitKey(1)