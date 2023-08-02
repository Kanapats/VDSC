# 08-01-2023
# Mr.Kanapat Appamatta

import cv2
import mediapipe as mp
import serial

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

SERIAL_PORT = 'COMX'
BAUD_RATE = 115200

ser = serial.Serial(SERIAL_PORT, BAUD_RATE)

def detect_pose(pose_landmarks):
    left_ankle = pose_landmarks[mp_pose.PoseLandmark.LEFT_ANKLE]
    right_ankle = pose_landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE]
    left_hip = pose_landmarks[mp_pose.PoseLandmark.LEFT_HIP]
    right_hip = pose_landmarks[mp_pose.PoseLandmark.RIGHT_HIP]

    hip_to_ankle_distance = abs(left_hip.y - left_ankle.y) + abs(right_hip.y - right_ankle.y)

    if hip_to_ankle_distance < 0.4:
        return "Danger"
    else:
        return "Normal"

def skeleton(frame, pose_landmarks):
    connections = mp_pose.POSE_CONNECTIONS
    for connection in connections:
        x0, y0 = int(pose_landmarks[connection[0]].x * frame.shape[1]), int(pose_landmarks[connection[0]].y * frame.shape[0])
        x1, y1 = int(pose_landmarks[connection[1]].x * frame.shape[1]), int(pose_landmarks[connection[1]].y * frame.shape[0])
        cv2.line(frame, (x0, y0), (x1, y1), (0, 255, 0), 2)

def logo(frame):
    logo = cv2.imread("logo.png")
    logo = cv2.resize(logo, (200, 150))
    frame_height, frame_width, _ = frame.shape
    logo_height, logo_width, _ = logo.shape
    offset_x = frame_width - logo_width - 10
    offset_y = frame_height - logo_height - 10
    
    frame[offset_y:offset_y + logo_height, offset_x:offset_x + logo_width] = cv2.addWeighted(frame[offset_y:offset_y + logo_height, offset_x:offset_x + logo_width], 1, logo, 1, 0)

def main():
    webcam = cv2.VideoCapture(X)

    cv2.namedWindow("Fall Detection", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Fall Detection", 640, 480)

    while True:
        ret, frame = webcam.read()

        if not ret:
            break

        frame = cv2.flip(frame, 1)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)

        if results.pose_landmarks:
            pose_landmarks = results.pose_landmarks.landmark
            image_height, image_width, _ = frame.shape

            skeleton(frame, pose_landmarks)

            pose_status = detect_pose(pose_landmarks)

            print(f"Pose Status: {pose_status}")
            ser.write(pose_status.encode())

        logo(frame)
        cv2.imshow("Fall Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    webcam.release()
    cv2.destroyAllWindows()
    ser.close()

if __name__ == "__main__":
    main()