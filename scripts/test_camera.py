#!/usr/bin/env python3
"""
Camera Test Script for Drowsiness Detection System
Used to verify that the camera is working properly and measure performance
"""
import cv2
import time
import sys
import os
import argparse

# Add parent directory to path for importing config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.utils import load_config, setup_logging

def test_camera(camera_index=None, resolution=None):
    """
    Test the camera by displaying a live video feed with performance metrics.
    
    Args:
        camera_index (int, optional): Camera device index to use
        resolution (tuple, optional): Desired resolution (width, height)
    
    Returns:
        bool: True if test completed successfully, False otherwise
    """
    logger = setup_logging()
    logger.info("Starting camera test...")
    
    # Load configuration
    try:
        config = load_config()
        logger.info("Configuration loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        print(f"ERROR: Failed to load configuration: {e}")
        return False
    
    # Override with function parameters if provided
    if camera_index is None:
        camera_index = config.get('camera_index', 0)
    
    if resolution is None:
        frame_width = config.get('frame_width', 640)
        frame_height = config.get('frame_height', 480)
    else:
        frame_width, frame_height = resolution
    
    print(f"Testing camera at index {camera_index}...")
    
    # Initialize camera
    cap = cv2.VideoCapture(camera_index)
    
    if not cap.isOpened():
        error_msg = f"ERROR: Could not open camera at index {camera_index}"
        logger.error(error_msg)
        print(error_msg)
        return False
    
    # Set camera properties
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
    
    # Display camera info
    actual_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    actual_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    nominal_fps = cap.get(cv2.CAP_PROP_FPS)
    
    print(f"Camera opened successfully:")
    print(f"- Requested resolution: {frame_width}x{frame_height}")
    print(f"- Actual resolution: {actual_width}x{actual_height}")
    print(f"- Nominal FPS: {nominal_fps}")
    print("Displaying camera feed. Press 'q' to exit, 's' to save a snapshot.")
    
    # Start timer for FPS calculation
    start_time = time.time()
    frame_count = 0
    fps = 0
    
    # Main loop
    while True:
        # Capture frame
        ret, frame = cap.read()
        
        if not ret:
            logger.error("Failed to grab frame from camera")
            print("ERROR: Failed to grab frame from camera")
            break
        
        # Calculate FPS
        frame_count += 1
        elapsed_time = time.time() - start_time
        if elapsed_time > 1.0:
            fps = frame_count / elapsed_time
            frame_count = 0
            start_time = time.time()
        
        # Add information overlay
        info_frame = frame.copy()
        cv2.putText(info_frame, f"Camera: {camera_index}", (10, 30),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(info_frame, f"Resolution: {actual_width}x{actual_height}", (10, 60),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(info_frame, f"FPS: {fps:.2f}", (10, 90),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Display the frame
        cv2.imshow("Camera Test", info_frame)
        
        # Process key presses
        key = cv2.waitKey(1) & 0xFF
        
        # 'q' key to quit
        if key == ord('q'):
            logger.info("Camera test stopped by user")
            break
            
        # 's' key to save a snapshot
        elif key == ord('s'):
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            snapshot_path = f"camera_test_{timestamp}.jpg"
            cv2.imwrite(snapshot_path, frame)
            logger.info(f"Saved camera snapshot to {snapshot_path}")
            print(f"Snapshot saved to {snapshot_path}")
    
    # Clean up
    cap.release()
    cv2.destroyAllWindows()
    logger.info("Camera test complete")
    print("Camera test complete.")
    return True

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Test camera for drowsiness detection")
    parser.add_argument("-c", "--camera", type=int, help="Camera index to use")
    parser.add_argument("-r", "--resolution", type=str, help="Desired resolution (WxH)")
    
    args = parser.parse_args()
    
    # Parse resolution if provided
    resolution = None
    if args.resolution:
        try:
            width, height = map(int, args.resolution.split("x"))
            resolution = (width, height)
        except ValueError:
            print("ERROR: Resolution must be in format WxH (e.g., 640x480)")
            sys.exit(1)
    
    # Run the test
    success = test_camera(args.camera, resolution)
    sys.exit(0 if success else 1)