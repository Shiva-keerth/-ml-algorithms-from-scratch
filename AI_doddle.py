import cv2
import numpy as np
import mediapipe as mp

# Camera setup
cap = cv2.VideoCapture(0)

# MediaPipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.85,
    min_tracking_confidence=0.5
)
mp_draw = mp.solutions.drawing_utils

# Initialize canvas later after frame size known
canvas = None
current_color = (0, 0, 255)  # Default color (Red)
prev_x, prev_y = 0, 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    # Initialize canvas dynamically
    if canvas is None:
        canvas = np.zeros_like(frame)

    # Convert BGR to RGB for MediaPipe
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    # --- TOP UI BAR ---
    cv2.rectangle(frame, (0, 0), (640, 65), (50, 50, 50), -1)

    # Color buttons
    cv2.rectangle(frame, (10, 10), (110, 55), (255, 0, 0), -1)  # Blue
    cv2.rectangle(frame, (130, 10), (230, 55), (0, 255, 0), -1)  # Green
    cv2.rectangle(frame, (250, 10), (350, 55), (0, 0, 255), -1)  # Red
    cv2.rectangle(frame, (370, 10), (470, 55), (0, 0, 0), -1)  # Eraser

    # CLEAR button
    cv2.rectangle(frame, (500, 10), (628, 55), (255, 255, 255), 1)
    cv2.putText(frame, "CLEAR", (510, 42),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            # Draw hand skeleton
            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

            lm = hand.landmark
            h, w, _ = frame.shape

            # Index & Middle finger tips coordinates
            ix, iy = int(lm[8].x * w), int(lm[8].y * h)
            mx, my = int(lm[12].x * w), int(lm[12].y * h)

            # Check if index finger is up
            if lm[8].y < lm[6].y:

                # Selection Mode (2 Fingers up: Index and Middle)
                if lm[12].y < lm[10].y:
                    prev_x, prev_y = 0, 0

                    if iy < 65:
                        if 10 < ix < 110:
                            current_color = (255, 0, 0)  # Blue
                        elif 130 < ix < 230:
                            current_color = (0, 255, 0)  # Green
                        elif 250 < ix < 350:
                            current_color = (0, 0, 255)  # Red
                        elif 370 < ix < 470:
                            current_color = (0, 0, 0)  # Eraser
                        elif 500 < ix < 620:
                            canvas = np.zeros_like(frame)  # Clear Canvas

                    # Selection indicator
                    cv2.circle(frame, (ix, iy), 15, current_color, cv2.FILLED)

                # Drawing Mode (Only 1 finger up)
                else:
                    if prev_x != 0 and prev_y != 0:
                        ix = int(prev_x * 0.7 + ix * 0.3)
                        iy = int(prev_y * 0.7 + iy * 0.3)

                    cv2.circle(frame, (ix, iy), 10, current_color, cv2.FILLED)

                    if prev_x == 0 and prev_y == 0:
                        prev_x, prev_y = ix, iy

                    thickness = 25 if current_color == (0, 0, 0) else 6

                    cv2.line(canvas, (prev_x, prev_y), (ix, iy), current_color, thickness)

                    prev_x, prev_y = ix, iy
            else:
                prev_x, prev_y = 0, 0

    # Merge canvas + frame properly
    img_gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, img_inv = cv2.threshold(img_gray, 20, 255, cv2.THRESH_BINARY_INV)
    img_inv = cv2.cvtColor(img_inv, cv2.COLOR_GRAY2BGR)

    frame = cv2.bitwise_and(frame, img_inv)
    output = cv2.bitwise_or(frame, canvas)

    cv2.namedWindow("Air Drawing System",cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Air Drawing System",cv2.WND_PROP_FULLSCREEN,cv2.WND_PROP_FULLSCREEN)
    cv2.imshow("Air Drawing System",output)

    cv2.imshow("Air Drawing System", output)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()