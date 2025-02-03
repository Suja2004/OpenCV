import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7,
                       min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Initialize webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Set the screen size for pyautogui
screen_width, screen_height = pyautogui.size()

# Variables for smooth cursor movement
prev_x, prev_y = 0, 0
cursor_smoothness = 7  # Higher value = slower movement

# Variables for peace sign gesture detection
peace_sign_time = None


def fingers_status(hand_landmarks):
    """ Returns the status of the fingers (open or closed) """
    finger_tips = [
        mp_hands.HandLandmark.THUMB_TIP,
        mp_hands.HandLandmark.INDEX_FINGER_TIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp_hands.HandLandmark.RING_FINGER_TIP,
        mp_hands.HandLandmark.PINKY_TIP,
    ]

    finger_dips = [
        mp_hands.HandLandmark.THUMB_IP,
        mp_hands.HandLandmark.INDEX_FINGER_DIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_DIP,
        mp_hands.HandLandmark.RING_FINGER_DIP,
        mp_hands.HandLandmark.PINKY_DIP,
    ]

    fingers = []
    for tip, dip in zip(finger_tips, finger_dips):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[dip].y:
            fingers.append(True)  # Finger is open
        else:
            fingers.append(False)  # Finger is closed
    return fingers


def get_landmark_position(hand_landmarks, landmark_id):
    """ Returns the x, y coordinates of a landmark """
    h, w, _ = frame.shape
    return int(hand_landmarks.landmark[landmark_id].x * w), int(hand_landmarks.landmark[landmark_id].y * h)


def move_cursor(index_finger_tip):
    """ Move the mouse cursor smoothly to the index finger position on the full screen """
    global prev_x, prev_y
    x, y = index_finger_tip

    # Scale the x, y position to screen resolution
    screen_x = np.interp(x, [0, frame.shape[1]], [0, screen_width])
    screen_y = np.interp(y, [0, frame.shape[0]], [0, screen_height])

    # Smooth the cursor movement
    prev_x += (screen_x - prev_x) / cursor_smoothness
    prev_y += (screen_y - prev_y) / cursor_smoothness
    pyautogui.moveTo(prev_x, prev_y)


def left_click():
    """ Perform left click """
    pyautogui.click()


def right_click():
    """ Perform right click """
    pyautogui.rightClick()


def scroll(direction):
    """ Scroll the page up or down """
    if direction == 'up':
        pyautogui.scroll(10)
    elif direction == 'down':
        pyautogui.scroll(-10)


def handle_peace_sign(fingers):
    """ Handle Peace Sign gesture to stop the program """
    global peace_sign_time
    if fingers[1] and fingers[2] and not any(fingers[3:]):  # Peace Sign (Index + Middle)
        if peace_sign_time is None:
            peace_sign_time = time.time()  
        elif time.time() - peace_sign_time > 1:  
            print("Stopping the program...")
            return True
    else:
        peace_sign_time = None  
    return False


while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame. Exiting...")
        break

    frame = cv2.flip(frame, 1)  # Flip the frame horizontally
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process frame with MediaPipe Hands
    results = hands.process(rgb_frame)

    action = "No Action"
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get the status of the fingers
            fingers = fingers_status(hand_landmarks)
            index_finger_tip = get_landmark_position(hand_landmarks, mp_hands.HandLandmark.INDEX_FINGER_TIP)
            thumb_tip = get_landmark_position(hand_landmarks, mp_hands.HandLandmark.THUMB_TIP)
            pinky_tip = get_landmark_position(hand_landmarks, mp_hands.HandLandmark.PINKY_TIP)
            middle_finger_tip = get_landmark_position(hand_landmarks, mp_hands.HandLandmark.MIDDLE_FINGER_TIP)
            ring_finger_tip = get_landmark_position(hand_landmarks, mp_hands.HandLandmark.RING_FINGER_TIP)

            # Check gestures
            if all(fingers):  # Fingers Up = Scroll Up
                scroll('up')
                action = "Scrolling Up"
            elif not any(fingers):  # Fingers Down = Scroll Down
                scroll('down')
                action = "Scrolling Down"
            elif fingers[0] and not any(fingers[1:]):  # Fist = Left click
                left_click()
                action = "Left Click"
            elif fingers[0] and fingers[1] and not any(fingers[2:]):  # Thumbs Up = Right click
                right_click()
                action = "No Action - Placeholder"
            elif fingers[1] and not any(fingers[2:]):  # Index finger only = Move cursor
                move_cursor(index_finger_tip)
                action = "Moving Cursor"

            elif fingers[1] and fingers[2] and fingers[3] and fingers[
                4]:  # All fingers extended 
                action = "Moving Cursor"
            elif fingers[0] and fingers[4] and not any(fingers[2:3]):  # Thumb + Middle 
                action = "Right Click"

            # Handle Peace Sign Gesture to stop the program
            if handle_peace_sign(fingers):
                cap.release()
                cv2.destroyAllWindows()

            # Display action text on the frame
            cv2.putText(frame, f"Action: {action}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Show the frame with action text
    cv2.imshow("Hand Gesture Control", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Manually exit by pressing 'q'
        print("Exiting...")
        break

cap.release()
cv2.destroyAllWindows()
