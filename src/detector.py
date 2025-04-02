"""
Real-time Drowsiness Detection System using OpenCV and dlib
"""
import cv2
import dlib
import time
import numpy as np
from .eye_aspect_ratio import calculate_ear
from .utils import load_config, setup_logging
from .facial_landmarks import get_facial_landmarks, draw_landmarks

class DrowsinessDetector:
    """
    Main class for drowsiness detection using eye aspect ratio analysis.
    
    This detector tracks facial landmarks and analyzes eye openness to detect 
    signs of drowsiness in real-time video feed.
    """
    
    def __init__(self, config_path=None):
        """
        Initialize the drowsiness detector with the given configuration.
        
        Args:
            config_path (str, optional): Path to configuration file. 
                                         If None, default config will be used.
        """
        # Setup logger
        self.logger = setup_logging()
        self.logger.info("Initializing Drowsiness Detection System")
        
        # Load configuration
        self.config = load_config(config_path)
        
        # Initialize face detector and landmark predictor
        self.detector = dlib.get_frontal_face_detector()
        try:
            self.predictor = dlib.shape_predictor(self.config['landmark_path'])
            self.logger.info(f"Loaded facial landmark predictor from {self.config['landmark_path']}")
        except RuntimeError as e:
            self.logger.error(f"Failed to load facial landmark predictor: {e}")
            raise
            
        # Configure drowsiness detection parameters
        self.EAR_THRESHOLD = self.config['ear_threshold']
        self.EAR_FRAMES = self.config['ear_frames']
        self.logger.info(f"Detection parameters: EAR threshold={self.EAR_THRESHOLD}, frames={self.EAR_FRAMES}")
        
        # Initialize counters
        self.frame_counter = 0  # Consecutive frames with closed eyes
        self.alert_counter = 0  # Total number of drowsiness alerts
        
        # Performance metrics
        self.fps = 0
        self.frame_count = 0
        self.start_time = time.time()
        
    def run(self):
        """
        Run the drowsiness detection loop on video feed from camera.
        
        This method continuously processes video frames, detects faces,
        analyzes eye aspect ratio, and triggers alerts when drowsiness is detected.
        """
        # Initialize camera
        camera_index = self.config.get('camera_index', 0)
        cap = cv2.VideoCapture(camera_index)
        
        if not cap.isOpened():
            self.logger.error(f"Failed to open camera at index {camera_index}")
            raise RuntimeError(f"Could not open camera at index {camera_index}")
            
        # Configure camera
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.config.get('frame_width', 640))
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config.get('frame_height', 480))
        
        self.logger.info(f"Camera initialized at index {camera_index}")
        self.logger.info("Starting detection loop")
        
        try:
            while True:
                # Capture frame
                ret, frame = cap.read()
                if not ret:
                    self.logger.error("Failed to capture frame from camera")
                    break
                
                # Process the frame
                processed_frame = self._process_frame(frame)
                
                # Update FPS calculation
                self._update_fps()
                
                # Display FPS if enabled
                if self.config.get('show_fps', True):
                    cv2.putText(processed_frame, f"FPS: {self.fps:.2f}", 
                               (processed_frame.shape[1] - 120, 30),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                # Display the frame
                cv2.imshow("Drowsiness Detection", processed_frame)
                
                # Check for key press (q to quit)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.logger.info("Detection stopped by user")
                    break
                    
        except Exception as e:
            self.logger.error(f"Error in detection loop: {e}")
        finally:
            # Clean up resources
            cap.release()
            cv2.destroyAllWindows()
            self.logger.info("Drowsiness detection ended")
            
    def _process_frame(self, frame):
        """
        Process a single frame for drowsiness detection.
        
        Args:
            frame: The video frame to process
            
        Returns:
            The processed frame with visualizations
        """
        # Create a copy of the frame for visualization
        viz_frame = frame.copy()
        
        # Convert to grayscale for face detection (improves performance)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = self.detector(gray, 0)
        
        if len(faces) == 0:
            # No face detected
            cv2.putText(viz_frame, "No face detected", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        for face in faces:
            # Get facial landmarks
            landmarks = get_facial_landmarks(self.predictor, gray, face)
            
            # Draw facial landmarks if enabled
            if self.config.get('show_landmarks', True):
                viz_frame = draw_landmarks(viz_frame, landmarks)
            
            # Extract eye landmarks
            left_eye = landmarks[42:48]   # Left eye landmarks (dlib points 42-47)
            right_eye = landmarks[36:42]  # Right eye landmarks (dlib points 36-41)
            
            # Calculate eye aspect ratios
            left_ear = calculate_ear(left_eye)
            right_ear = calculate_ear(right_eye)
            
            # Average the eye aspect ratios
            ear = (left_ear + right_ear) / 2.0
            
            # Display EAR value if enabled
            if self.config.get('show_ear', True):
                cv2.putText(viz_frame, f"EAR: {ear:.2f}", (300, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            
            # Check if EAR is below threshold (eyes are closing)
            if ear < self.EAR_THRESHOLD:
                # Increment drowsy frame counter
                self.frame_counter += 1
                
                # Display drowsy frame count
                cv2.putText(viz_frame, f"Drowsy frames: {self.frame_counter}", (10, 60),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                
                # Check if drowsiness threshold is reached
                if self.frame_counter >= self.EAR_FRAMES:
                    # Drowsiness detected!
                    self.alert_counter += 1
                    self._trigger_alert(viz_frame)
            else:
                # Reset counter if eyes are open
                self.frame_counter = 0
        
        return viz_frame
    
    def _trigger_alert(self, frame):
        """
        Trigger drowsiness alert with visual and optional audio cues.
        
        Args:
            frame: The current video frame for visualization
        """
        # Display drowsiness alert text
        cv2.putText(frame, "DROWSINESS ALERT!", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        # Add red overlay to the frame (visual alert)
        red_overlay = frame.copy()
        cv2.rectangle(red_overlay, (0, 0), (frame.shape[1], frame.shape[0]), 
                     (0, 0, 255), -1)
        cv2.addWeighted(red_overlay, 0.2, frame, 0.8, 0, frame)
        
        # Log the alert
        self.logger.warning(f"Drowsiness detected! Alert #{self.alert_counter}")
        
        # Play sound alert if enabled
        if self.config.get('use_sound_alert', False):
            # Sound alert would be implemented here
            # This is a placeholder for actual sound implementation
            pass
    
    def _update_fps(self):
        """Update the FPS (frames per second) calculation"""
        self.frame_count += 1
        elapsed_time = time.time() - self.start_time
        
        # Update FPS every second
        if elapsed_time > 1.0:
            self.fps = self.frame_count / elapsed_time
            self.frame_count = 0
            self.start_time = time.time()

if __name__ == "__main__":
    detector = DrowsinessDetector()
    detector.run()