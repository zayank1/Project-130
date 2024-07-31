import cv2
import mediapipe as mp
from pynput.keyboard import Key, Controller

keyboard = Controller()

cap = cv2.VideoCapture(0)

#Un comment  the corect code 

#Width  = int(cap.get(cv2.CAP_PROP_FRAME_Height)) 
#Height  = int(cap.get(cv2.CAP_PROP_FRAME_Width))

width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) 
height  = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) 

#width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) 
#height  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

#width  = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) 
#height  = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)

tipIds = [4, 8, 12, 16, 20]

state = None

# Define a function to count fingers
def countFingers(image, hand_landmarks, handNo=0):

    global state

    if hand_landmarks:
        # Get all Landmarks of the FIRST Hand VISIBLE
        landmarks = hand_landmarks[handNo].landmark

        # Count Fingers        
        fingers = []

        for lm_index in tipIds:
                # Get Finger Tip and Bottom y Position Value
                finger_tip_y = landmarks[lm_index].y 
                finger_bottom_y = landmarks[lm_index - 2].y

                # Check if ANY FINGER is OPEN or CLOSED
                if lm_index !=4:
                    if finger_tip_y < finger_bottom_y:
                        fingers.append(1)
                        # print("FINGER with id ",lm_index," is Open")

                    if finger_tip_y > finger_bottom_y:
                        fingers.append(0)
                        # print("FINGER with id ",lm_index," is Closed")

        
        totalFingers = fingers.count(1)
      
        # Control presentation
        #Un comment  the corect code below

        #finger_tip_y = (landmarks[8].x)*width
        #finger_tip_x = (landmarks[8].y)*height

        #finger_tip_x = (landmarks[8].x)*height
        #finger_tip_y = (landmarks[8].y)*width

        finger_tip_x = (landmarks[8].x)*width
        finger_tip_y = (landmarks[8].y)*height

        #finger_tip_x = (landmarks[8].x)*Width
        #finger_tip_y = (landmarks[8].y)*Height
        
        
        if totalFingers >= 1:
            if  finger_tip_x < height-250:
                print("scroll Up")
                keyboard.press(Key.up)

            if finger_tip_x > height-250:
                print("Scroll Down")
                keyboard.press(Key.down)
       
        
        
# Define a function to 
def drawHandLanmarks(image, hand_landmarks):

    # Darw connections between landmark points
    if hand_landmarks:

      for landmarks in hand_landmarks:
               
        mp_drawing.draw_landmarks(image, landmarks, mp_hands.HAND_CONNECTIONS)



while True:
    success, image = cap.read()

    image = cv2.flip(image, 1)
    
    # Detect the Hands Landmarks 
    results = hands.process(image)

    # Get landmark position from the processed result
    hand_landmarks = results.multi_hand_landmarks

    # Draw Landmarks
    drawHandLanmarks(image, hand_landmarks)

    # Get Hand Fingers Position        
    countFingers(image, hand_landmarks)

    cv2.imshow("Media Controller", image)

    # Quit the window on pressing Sapcebar key
    key = cv2.waitKey(1)
    if key == 32:
        break

cv2.destroyAllWindows()
