# imgen_logger.py
import logging
import os

def setup_logging(log_file_path):
    # Create a custom logger
    logger = logging.getLogger('imgen_logger')
    logger.setLevel(logging.DEBUG)  # Set the lowest threshold for the logger

    # Check if logger already has handlers to avoid duplicate logs
    if not logger.handlers:
        # Create handlers
        console_handler = logging.StreamHandler()
        file_handler = logging.FileHandler(log_file_path)

        # Set the logging level for handlers
        console_handler.setLevel(logging.INFO)
        file_handler.setLevel(logging.DEBUG)

        # Create formatters and add them to handlers
        console_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        console_handler.setFormatter(console_formatter)
        file_handler.setFormatter(file_formatter)

        # Add handlers to the logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    
    return logger

# Set up logging and get the logger instance
# log_file = os.path.expanduser('.imgen.log')
log_file = os.path.join(os.getcwd(), '.imgen.log')
print(f'Logging to {log_file}')
logger = setup_logging(log_file)
