
import cv2
import time
import numpy as np
import threading

# Try to import mediapipe - better than dlib, no extra file needed
try:
    import mediapipe as mp
    HAS_MEDIAPIPE = True
except:
    HAS_MEDIAPIPE = False

# ===== LOUD ALARM SOUND SYSTEM =====
try:
    import winsound
    HAS_WINSOUND = True
except:
    HAS_WINSOUND = False

try:
    import pygame
    pygame.mixer.init()
    HAS_PYGAME = True
    # Load alarm sound if exists
    try:
        pygame.mixer.music.load('/mnt/data/alarm.wav')
    except:
        pass
except:
    HAS_PYGAME = False

alarm_playing = False

def play_alarm_sound():
    """Play loud alarm sound in loop"""
    global alarm_playing
    if alarm_playing:
        return
    alarm_playing = True
    
    def _play():
        global alarm_playing
        try:
            if HAS_WINSOUND:
                # Windows beep - very loud and continuous
                for _ in range(8):  # Beep 8 times loudly
                    if not alarm_playing:
                        break
                    winsound.Beep(1000, 500)  # 1000Hz for 500ms
                    winsound.Beep(1500, 500)  # 1500Hz for 500ms - siren effect
                    time.sleep(0.1)
            elif HAS_PYGAME:
                pygame.mixer.music.play(loops=5)
                time.sleep(3)
            else:
                # Fallback - system bell
                for _ in range(10):
                    if not alarm_playing:
                        break
                    print('\a\a\a WAKE UP!!! DROWSINESS DETECTED!!! \a\a\a')
                    time.sleep(0.3)
        except Exception as e:
            print(f"Alarm error: {e}")
        finally:
            alarm_playing = False
    
    thread = threading.Thread(target=_play, daemon=True)
    thread.start()

def stop_alarm_sound():
    global alarm_playing
    alarm_playing = False
    try:
        if HAS_PYGAME:
            pygame.mixer.music.stop()
    except:
        pass

print("="*60)
print("DROWSINESS DETECTION - FINAL LAPTOP FIXED VERSION")
print("="*60)

# Function to find working camera
def find_camera():
    print("\nSearching for camera...")
    # Try different indexes
    for i in [0, 1, 2, 3, 4]:
        print(f"Trying camera index {i}...")
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)  # CAP_DSHOW for Windows
        if cap.isOpened():
            ret, frame = cap.read()
            if ret and frame is not None:
                print(f"SUCCESS! Camera found at index {i}")
                return cap
            cap.release()
    
    # Try IP Webcam (phone as camera) - common IPs
    print("\nLaptop camera not found, trying phone camera...")
    phone_urls = [
        "http://192.168.1.2:8080/video",
        "http://192.168.1.3:8080/video",
        "http://192.168.1.4:8080/video",
        "http://192.168.1.5:8080/video",
        "http://192.168.1.6:8080/video",
        "http://192.168.1.7:8080/video",
        "http://192.168.0.2:8080/video",
        "http://192.168.43.1:8080/video"
    ]
    for url in phone_urls:
        try:
            print(f"Trying phone URL: {url}")
            cap = cv2.VideoCapture(url)
            cap.set(cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 2000)
            ret, frame = cap.read()
            if ret:
                print(f"SUCCESS! Phone camera found at {url}")
                return cap
            cap.release()
        except:
            pass
            
    return None

# Try to get camera
cap = find_camera()

if cap is None:
    print("\n" + "="*60)
    print("CAMERA STILL NOT FOUND - BUT DON'T WORRY!")
    print("="*60)
    print("\nYour laptop camera driver is still missing after update.")
    print("\n3 OPTIONS TO FIX FOR FYP DEMO:")
    print("\nOPTION 1 - PHONE AS CAMERA (100% WORKS - 2 MIN):")
    print("1. On PHONE: Install 'IP Webcam' app from Play Store")
    print("2. Open app -> Click 'Start server' at bottom")
    print("3. It shows IP like http://192.168.1.5:8080")
    print("4. On LAPTOP: Edit this file line 28:")
    print("   cap = cv2.VideoCapture('http://YOUR_PHONE_IP:8080/video')")
    print("5. Run again: python main_final_laptop_fixed.py")
    print("\nOPTION 2 - USE VIDEO FILE FOR DEMO:")
    print("   cap = cv2.VideoCapture('demo_video.mp4')")
    print("\nOPTION 3 - REINSTALL CAMERA DRIVER:")
    print("1. Device Manager -> Action -> Scan for hardware changes")
    print("2. Right-click Unknown device -> Update driver -> Search automatically")
    print("3. Press Fn + F8 (camera key) on keyboard")
    print("4. Check physical slider on top of screen - slide LEFT")
    print("="*60)
    # Create demo mode with video file or image
    print("\nRunning in DEMO IMAGE mode for now...")
    # Create a dummy window
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    cv2.putText(img, "CAMERA NOT FOUND", (150, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
    cv2.putText(img, "Use Phone as Camera", (140, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
    cv2.putText(img, "See instructions in CMD", (130, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
    cv2.imshow("Drowsiness Detection - Fix Camera", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    exit()

# If camera found, run drowsiness detection
print("\nStarting Drowsiness Detection...")
print("Press 'q' to quit, 's' to save screenshot")

if HAS_MEDIAPIPE:
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)
    mp_drawing = mp.solutions.drawing_utils
    # Eye landmarks for EAR calculation
    LEFT_EYE = [33, 160, 158, 133, 153, 144]
    RIGHT_EYE = [362, 385, 387, 263, 373, 380]
    
    def eye_aspect_ratio(landmarks, eye_indices):
        # Calculate EAR
        p = []
        for idx in eye_indices:
            p.append(landmarks[idx])
        # vertical distances
        v1 = np.linalg.norm(np.array([p[1].x, p[1].y]) - np.array([p[5].x, p[5].y]))
        v2 = np.linalg.norm(np.array([p[2].x, p[2].y]) - np.array([p[4].x, p[4].y]))
        # horizontal distance
        h = np.linalg.norm(np.array([p[0].x, p[0].y]) - np.array([p[3].x, p[3].y]))
        ear = (v1 + v2) / (2.0 * h)
        return ear

    EAR_THRESHOLD = 0.25
    CONSEC_FRAMES = 20
    counter = 0
    alarm_on = False

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to read frame")
            break
            
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)
        h, w, _ = frame.shape
        
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                left_ear = eye_aspect_ratio(face_landmarks.landmark, LEFT_EYE)
                right_ear = eye_aspect_ratio(face_landmarks.landmark, RIGHT_EYE)
                ear = (left_ear + right_ear) / 2.0
                
                # Draw eye landmarks
                for idx in LEFT_EYE + RIGHT_EYE:
                    lm = face_landmarks.landmark[idx]
                    cv2.circle(frame, (int(lm.x * w), int(lm.y * h)), 2, (0,255,0), -1)
                
                cv2.putText(frame, f"EAR: {ear:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
                
                if ear < EAR_THRESHOLD:
                    counter += 1
                    if counter >= CONSEC_FRAMES:
                        if not alarm_on:  # Only play once when first detected
                            play_alarm_sound()
                        alarm_on = True
                        cv2.putText(frame, "DROWSINESS ALERT!", (150, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,0,255), 3)
                        cv2.putText(frame, "WAKE UP!", (250, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                        cv2.putText(frame, "ALARM ON! BEEP BEEP!", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
                else:
                    counter = 0
                    if alarm_on:
                        stop_alarm_sound()
                    alarm_on = False
                    cv2.putText(frame, "AWAKE - Eyes Open", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)
        else:
            cv2.putText(frame, "No Face Detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

        cv2.imshow("Drowsiness Detection - FINAL FIXED", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            cv2.imwrite(f"screenshot_{int(time.time())}.jpg", frame)
            print("Screenshot saved!")

else:
    # Fallback simple face detection without mediapipe
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        for (x,y,w,h) in faces:
            cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color, (ex,ey), (ex+ew, ey+eh), (0,255,0), 2)
        
        cv2.putText(frame, "Face Detected - Install mediapipe for EAR", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
        cv2.imshow("Drowsiness Detection - Simple Mode", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
print("Program closed successfully!")
