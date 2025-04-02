"""
Facial landmark detection and visualization for drowsiness detection.
"""
import dlib
import cv2
import numpy as np

def shape_to_np(shape, dtype="int"):
    """
    Convert dlib's shape object to numpy array.
    
    Args:
        shape: dlib shape object containing facial landmarks
        dtype: data type for the output array
        
    Returns:
        numpy.ndarray: Array of (x, y) coordinates of landmarks
    """
    # Initialize the array of (x, y) coordinates
    coords = np.zeros((shape.num_parts, 2), dtype=dtype)
    
    # Loop over all facial landmarks and convert them to (x, y) coordinates
    for i in range(0, shape.num_parts):
        coords[i] = (shape.part(i).x, shape.part(i).y)
        
    return coords

def get_facial_landmarks(predictor, frame, face):
    """
    Detect facial landmarks from a face region.
    
    Args:
        predictor: dlib shape predictor
        frame: input image frame (grayscale)
        face: dlib face rectangle
        
    Returns:
        numpy.ndarray: Array of facial landmark coordinates
    """
    # Run the landmark predictor on the face region
    shape = predictor(frame, face)
    
    # Convert landmarks to a numpy array
    landmarks = shape_to_np(shape)
    
    return landmarks

def draw_landmarks(frame, landmarks):
    """
    Draw facial landmarks and eye regions on the frame.
    
    Args:
        frame: input image frame
        landmarks: numpy array of facial landmark coordinates
        
    Returns:
        numpy.ndarray: Frame with landmarks visualized
    """
    # Create a copy of the frame to draw on
    viz_frame = frame.copy()
    
    # Draw all facial landmarks as small circles
    for (x, y) in landmarks:
        cv2.circle(viz_frame, (x, y), 1, (0, 255, 0), -1)
    
    # Extract eye landmark points
    left_eye = landmarks[42:48]   # Left eye landmarks (points 42-47)
    right_eye = landmarks[36:42]  # Right eye landmarks (points 36-41)
    
    # Define the convex hulls of the eyes
    left_eye_hull = cv2.convexHull(left_eye)
    right_eye_hull = cv2.convexHull(right_eye)
    
    # Draw the convex hulls of the eyes
    cv2.drawContours(viz_frame, [left_eye_hull], -1, (0, 255, 0), 1)
    cv2.drawContours(viz_frame, [right_eye_hull], -1, (0, 255, 0), 1)
    
    # Label the eyes
    left_eye_center = left_eye.mean(axis=0).astype("int")
    right_eye_center = right_eye.mean(axis=0).astype("int")
    
    cv2.putText(viz_frame, "L", (left_eye_center[0] - 10, left_eye_center[1] - 10),
              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    cv2.putText(viz_frame, "R", (right_eye_center[0] - 10, right_eye_center[1] - 10),
              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    
    return viz_frame