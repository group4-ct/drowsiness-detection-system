import numpy as np
from scipy.spatial import distance as dist

def calculate_ear(eye):
    """
    Calculate the eye aspect ratio (EAR) given eye landmarks.
    
    The EAR is computed as the ratio of the height of the eye to its width.
    
    Args:
        eye: numpy array of shape (6, 2) containing the (x, y) coordinates of the 6 eye landmarks
        
    Returns:
        float: Eye aspect ratio value
        
    Reference:
        Soukupová and Čech (2016) - Real-Time Eye Blink Detection Using Facial Landmarks
    """
    # Compute the euclidean distances between the two sets of vertical eye landmarks
    A = dist.euclidean(eye[1], eye[5])  # Distance between landmarks 1 and 5
    B = dist.euclidean(eye[2], eye[4])  # Distance between landmarks 2 and 4
    
    # Compute the euclidean distance between the horizontal eye landmarks
    C = dist.euclidean(eye[0], eye[3])  # Distance between landmarks 0 and 3
    
    # Calculate the eye aspect ratio
    ear = (A + B) / (2.0 * C)
    
    return ear