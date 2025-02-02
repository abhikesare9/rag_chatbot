import logging
import threading

class SingletonLogger:
    _instance = None
    _lock = threading.Lock()  # Ensures thread safety

    def __new__(cls, log_file="app.log"):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(SingletonLogger, cls).__new__(cls)
                
                # Configure the logger
                cls._instance.logger = logging.getLogger("SingletonLogger")
                cls._instance.logger.setLevel(logging.DEBUG)

                # Create file handler
                file_handler = logging.FileHandler(log_file)
                file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

                # Create console handler
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

                # Add handlers to logger
                cls._instance.logger.addHandler(file_handler)
                cls._instance.logger.addHandler(console_handler)

        return cls._instance

    def get_logger(self):
        return self.logger
    

if __name__ =="__main__":
    logger = SingletonLogger().get_logger()
    logger.info("this is info")
    

