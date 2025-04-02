#!/usr/bin/env python3
"""
Real-time Drowsiness Detection System
Main entry point for the application

This script initializes and runs the drowsiness detection system.
It handles the high-level application flow and error handling.
"""
import sys
import traceback
from src.detector import DrowsinessDetector
from src.utils import setup_logging

def main():
    """Main application entry point"""
    # Setup logging
    logger = setup_logging()
    logger.info("Starting Drowsiness Detection System...")
    
    try:
        # Initialize the drowsiness detector
        detector = DrowsinessDetector()
        
        # Run the detection loop
        detector.run()
        
    except KeyboardInterrupt:
        # Handle manual interruption gracefully
        logger.info("Drowsiness Detection System interrupted by user")
        
    except Exception as e:
        # Log any unhandled exceptions
        logger.error(f"Error in Drowsiness Detection System: {e}")
        logger.error(traceback.format_exc())
        return 1
        
    finally:
        # Always log when stopping
        logger.info("Drowsiness Detection System stopped")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())