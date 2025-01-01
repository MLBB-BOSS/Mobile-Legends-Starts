import logging

def setup_logger(name='bot_logger', level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Create console handler with formatting
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(handler)
    
    return logger
