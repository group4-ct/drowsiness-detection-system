"""
Utility functions for the Drowsiness Detection System.
"""
import os
import yaml
import logging
from datetime import datetime

def load_config(config_path=None):
    """
    Load configuration from YAML file.
    
    This function loads the configuration settings from a YAML file
    and ensures that all paths are properly resolved.
    
    Args:
        config_path (str, optional): Path to the configuration file.
                                     If None, default config will be used.
    
    Returns:
        dict: Configuration settings
        
    Raises:
        FileNotFoundError: If the config file doesn't exist
        yaml.YAMLError: If the config file has invalid YAML
    """
    if config_path is None:
        # Default config path relative to the project root
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(base_dir, 'config', 'config.yaml')
    
    # Check if config file exists
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    # Load configuration from file
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error parsing configuration file: {e}")
    
    # Resolve relative paths in configuration
    if 'landmark_path' in config and not os.path.isabs(config['landmark_path']):
        config['landmark_path'] = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            config['landmark_path']
        )
    
    if 'sound_file' in config and not os.path.isabs(config['sound_file']):
        config['sound_file'] = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            config['sound_file']
        )
    
    return config

def setup_logging(log_to_file=True):
    """
    Set up logging configuration.
    
    This function configures the Python logging system to log messages
    to both the console and optionally to a file.
    
    Args:
        log_to_file (bool): Whether to log to a file in addition to console
        
    Returns:
        logging.Logger: Configured logger object
    """
    # Create logs directory if needed
    if log_to_file:
        logs_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'logs'
        )
        os.makedirs(logs_dir, exist_ok=True)
        
        # Create a timestamped log filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(logs_dir, f"drowsiness_detection_{timestamp}.log")
    
    # Configure logging
    logger = logging.getLogger('drowsiness_detector')
    logger.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Add console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Add file handler if requested
    if log_to_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.info(f"Logging to file: {log_file}")
    
    return logger