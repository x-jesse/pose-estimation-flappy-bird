import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Start capturing video from the webcam
cap = cv2.VideoCapture(0)

# Store previous positions of the left and right wrists
prev_left_wrist_y = None
prev_right_wrist_y = None

# Flapping detection threshold
flap_threshold = 40

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    # Convert the BGR image to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the image and detect the pose
    results = pose.process(image_rgb)

    if results.pose_landmarks:
        # Draw the pose landmarks on the original image
        mp_drawing.draw_landmarks(
            image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Get the positions of the left and right wrists
        left_wrist = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
        right_wrist = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]

        # Convert normalized landmark positions to pixel positions
        left_wrist_y = left_wrist.y * image.shape[0]
        right_wrist_y = right_wrist.y * image.shape[0]

        # Check for flapping motion
        if prev_left_wrist_y is not None and prev_right_wrist_y is not None:
            left_wrist_movement = abs(left_wrist_y - prev_left_wrist_y)
            right_wrist_movement = abs(right_wrist_y - prev_right_wrist_y)

            if left_wrist_movement > flap_threshold and right_wrist_movement > flap_threshold:
                cv2.putText(image, 'Flapping Detected', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        # Update previous wrist positions
        prev_left_wrist_y = left_wrist_y
        prev_right_wrist_y = right_wrist_y

    # Display the image with the pose landmarks
    cv2.imshow('MediaPipe Pose', image)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
