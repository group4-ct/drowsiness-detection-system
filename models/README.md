# Models Directory

This directory should contain the facial landmark predictor file used by dlib.

## Required Files

- `shape_predictor_68_face_landmarks.dat` - The facial landmark predictor file

## How to Get the Predictor File

1. Download the predictor file from the dlib website:
   http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2

2. Extract the .bz2 file to get the .dat file

3. Place the .dat file in this directory

Alternatively, you can use the following commands:

```bash
# On Linux/Mac
wget http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
bzip2 -d shape_predictor_68_face_landmarks.dat.bz2
mv shape_predictor_68_face_landmarks.dat models/

# On Windows (using PowerShell)
Invoke-WebRequest -Uri http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2 -OutFile shape_predictor_68_face_landmarks.dat.bz2
# Extract using 7-Zip or similar tool
# Move the .dat file to the models directory
```

The file is approximately 100MB in size.