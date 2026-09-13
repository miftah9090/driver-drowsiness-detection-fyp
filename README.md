
# 🚗 Driver Drowsiness Detection System - FYP

Real-time driver drowsiness detection using Python, OpenCV & MediaPipe. Detects closed eyes and triggers LOUD alarm to wake up driver.

## ✅ Features
- **Eye Aspect Ratio (EAR) Calculation** using MediaPipe Face Mesh
- **Real-time Detection**: EAR < 0.25 for 20 frames = DROWSY
- **LOUD Alarm Sound**: 1000Hz + 1500Hz siren beep (winsound + threading)
- **Works on HP/Lenovo** - Auto camera detection (index 0-4 + phone IP cam fallback)
- **Green eye landmarks** + RED alert: `DROWSINESS ALERT! WAKE UP!`

## 📸 Demo
![Demo](screenshot.png)
- Eyes Open: EAR ~0.30-0.35 = AWAKE
- Eyes Closed: EAR 0.04 = ALARM ON! BEEP BEEP!

## 🛠️ Installation

```bash
# Python 3.10.5 recommended
pip install opencv-python mediapipe==0.10.9 numpy pygame protobuf==3.20.3

# Or using requirements.txt
pip install -r requirements.txt
```

## ▶️ How to Run

```bash
python main_final_laptop_fixed.py
```

- Press `q` to quit
- Press `s` to save screenshot for FYP report
- Close eyes 2 sec -> Loud alarm!

## 🔊 Alarm System
- Uses `winsound.Beep()` on Windows (built-in, no extra file needed)
- Threading so camera doesn't freeze
- Auto stops when eyes open

## 🔧 Fixed Issues
- Fixed `0xA00F429E` camera error (HP/Lenovo)
- Fixed `Unknown device` driver issue
- Fixed mediapipe download timeout (`--default-timeout=1000`)

## 📁 Project Structure
```
DrowsyV2/
├── main_final_laptop_fixed.py
├── alarm.wav
├── requirements.txt
├── README.md
└── screenshots/
    ├── EAR_0.15_alert.jpg (your last photo)
    └── demo.mp4 (your video
```

## 🎓 FYP Details
- Student: Miftah Uddin
- University: Final Year Project 2023
- Tech: Python, OpenCV, MediaPipe Face Mesh, EAR Algorithm

## 📜 License
MIT - For educational FYP use
