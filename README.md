# Real-time Drowsiness Detection System

A real-time drowsiness detection system using Raspberry Pi 3B+, OpenCV, and dlib.

## Requirements

- Raspberry Pi 3B+
- USB Webcam
- Python 3.7+
- OpenCV
- dlib
- NumPy
- imutils

## Installation

1. Clone the repository:
```bash
git clone https://github.com/group4-ct/drowsiness-detection-system.git
cd drowsiness-detection-system
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download the facial landmark predictor:
Download the `shape_predictor_68_face_landmarks.dat` file and place it in the `models` directory.

## Usage

Run the main detection script:
```bash
python main.py
```

Or you can run the detector module directly:
```bash
python -m src.detector
```

## Configuration

Adjust the parameters in `config/config.yaml` to customize:
- Eye Aspect Ratio (EAR) threshold
- Number of frames for drowsiness detection
- Camera settings

## License

MIT License