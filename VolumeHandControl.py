import cv2
import time
import numpy as np
import math
import HandTrackingModule as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

cap = cv2.VideoCapture(0)

previous_time = 0

# New Hand Detector object
detector = htm.HandDetector(max_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Set connection with OS volume control device
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Read volume range
volume_range = volume.GetVolumeRange()
min_vol = volume_range[0]
max_vol = volume_range[1]


while True:
    # Get image from camera
    success, img = cap.read()

    # Use Hand Detector method to detect hand and draw in image
    img = detector.find_hands(img)

    # Find image position of all landmarks
    landmark_list = detector.find_position(img, draw=False)

    if len(landmark_list) != 0:
        # print(landmark_list[4], landmark_list[8])

        # select landmarks for the tip of the thumb and the tip of the pointer
        x1, y1 = landmark_list[4][1], landmark_list[4][2]
        x2, y2 = landmark_list[8][1], landmark_list[8][2]
        center_x, center_y = (x1 + x2) // 2, (y1 + y2) // 2

        # Mark specified points and connect with a line
        cv2.line(img, (x1, y1), (x2, y2), (255, 100, 100), 3)
        cv2.circle(img, (x1, y1), 8, (255, 50, 55), cv2.FILLED)
        cv2.circle(img, (x2, y2), 8, (255, 50, 55), cv2.FILLED)
        cv2.circle(img, (center_x, center_y), 5, (255, 50, 55), cv2.FILLED)

        # calculate the length of the line (distance between thumb and pointer points)
        length = math.hypot(x2 - x1, y2 - y1)
        # print(length)

        # update color of the center point depending on the length
        if length < 20 or length > 200:
            cv2.circle(img, (center_x, center_y), 5, (0, 255, 0), cv2.FILLED)

        # Convert points distance to volume range and adjust volume
        # Hand range 20-200 -> Volume range -96.0 - 0.0
        vol = np.interp(length, [20, 200], [min_vol, max_vol])

        volume.SetMasterVolumeLevel(int(vol), None)

    # Calculate ftp and display in image
    current_time = time.time()
    fps = 1/(current_time-previous_time)
    previous_time = current_time

    cv2.putText(img, f'FPS: {int(fps)}',
                (30, 50),  # image position
                cv2.FONT_HERSHEY_COMPLEX, 1,  # font and size
                (255, 0, 0), 2)  # text color and thickness

    # Output final image
    cv2.imshow("Image output", img)
    cv2.waitKey(1)
