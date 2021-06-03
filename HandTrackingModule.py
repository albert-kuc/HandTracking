import cv2
import mediapipe as mp
import time


class HandDetector:
    def __init__(self, mode=False, max_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5):

        # Define pretrained hands object
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(mode,
                                        max_hands,
                                        min_detection_confidence,
                                        min_tracking_confidence)

        # Draw points object
        self.mpDraw = mp.solutions.drawing_utils
        self.results = None

    def find_hands(self, img, draw=True):
        """
        Args:
            img:
            draw: Draws red hand landmark points and greed line connections between points
        """

        # Load image to hands object
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        # Extract information from results object
        if self.results.multi_hand_landmarks:  # if detects look up object

            for handLms in self.results.multi_hand_landmarks:

                # Display handLms in original image -> img
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def find_position(self, img, hand_number=0, draw=True):
        """
        Args:
            img:
            hand_number:
            draw: Draws purple hand landmark points
        """

        lm_list = []

        # Extract information from results object
        if self.results.multi_hand_landmarks:  # if detects look up object
            """Get idx number and ladnmark coordinates for specified hand"""

            my_hand = self.results.multi_hand_landmarks[hand_number]

            for idx, landmark in enumerate(my_hand.landmark):
                # landmark values are decimal places which is ratio of an image and not pixels
                # we need to multiply it with h, w of the image to get the pixel value
                h, w, c = img.shape
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                lm_list.append([idx, cx, cy])

                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

        return lm_list


def main():
    previous_time = 0

    # Create a video object to use web-cam no. 0 (diff no. for other web-cams)
    cap = cv2.VideoCapture(0)

    detector = HandDetector()

    while True:
        success, img = cap.read()  # that will give us our frame
        detector.find_hands(img, draw=True)
        landmarks_list = detector.find_position(img=img, draw=False)

        if len(landmarks_list) != 0:
            print(landmarks_list[3])  # landmarks range(0, 20) inclusive

        # calculate frame rate
        current_time = time.time()
        fps = 1/(current_time - previous_time)
        previous_time = current_time

        # include frame rate in img
        cv2.putText(img, str(int(fps)), (10, 70),  # display in img, fps to int, at position,
                    cv2.FONT_HERSHEY_PLAIN, 3,     # define font, define scale,
                    (255, 0, 255), 3)              # define color (purple), define thickness

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
