# 08-01-2023
# Mr.Kanapat Appamatta

import cv2
import numpy as np
import mediapipe as mp
import serial

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

SERIAL_PORT = 'COMX'
BAUD_RATE = 115200

ser = serial.Serial(SERIAL_PORT, BAUD_RATE)

def center(pose_landmarks, image_width, image_height):
    left_shoulder_x = int(pose_landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x * image_width)
    right_shoulder_x = int(pose_landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * image_width)
    center_x = (left_shoulder_x + right_shoulder_x) // 2
    left_hip_y = int(pose_landmarks[mp_pose.PoseLandmark.LEFT_HIP].y * image_height)
    right_hip_y = int(pose_landmarks[mp_pose.PoseLandmark.RIGHT_HIP].y * image_height)
    center_y = (left_hip_y + right_hip_y) // 2

    return center_x, center_y

def skeleton(frame, pose_landmarks):
    connections = mp_pose.POSE_CONNECTIONS
    for connection in connections:
        x0, y0 = int(pose_landmarks[connection[0]].x * frame.shape[1]), int(pose_landmarks[connection[0]].y * frame.shape[0])
        x1, y1 = int(pose_landmarks[connection[1]].x * frame.shape[1]), int(pose_landmarks[connection[1]].y * frame.shape[0])
        cv2.line(frame, (x0, y0), (x1, y1), (0, 255, 0), 2)

def logo(frame):
    logo = cv2.imread("logo.png")
    logo = cv2.resize(logo, (90, 90))
    frame_height, frame_width, _ = frame.shape
    logo_height, logo_width, _ = logo.shape
    offset_x = frame_width - logo_width - 10
    offset_y = frame_height - logo_height - 10
    
    frame[offset_y:offset_y + logo_height, offset_x:offset_x + logo_width] = cv2.addWeighted(frame[offset_y:offset_y + logo_height, offset_x:offset_x + logo_width], 1, logo, 1, 0)

def main():
    webcam = cv2.VideoCapture(X)

    cv2.namedWindow("Person Tracking", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Person Tracking", 640, 480)

    while True:
        ret, frame = webcam.read()

        if not ret:
            break

        frame = cv2.flip(frame, 0)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)

        if results.pose_landmarks:
            pose_landmarks = results.pose_landmarks.landmark
            image_height, image_width, _ = frame.shape

            center_x, center_y = center(pose_landmarks, image_width, image_height)

            skeleton(frame, pose_landmarks)
            cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

            print(f"Position {center_x}, {center_y}")
            position_str = f"{center_x},{center_y}\n"
            ser.write(position_str.encode())

        logo(frame)
        cv2.imshow("Person Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    webcam.release()
    cv2.destroyAllWindows()
    ser.close()

if __name__ == "__main__":
    main()