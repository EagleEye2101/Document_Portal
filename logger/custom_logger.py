import logging
import os
from datetime import datetime

class CustomLogger:
    def __init__(self,log_dir="logs"):
        # ensure logs directory exists
        self.log.dir = os.path.join(os.getcwd(),log_dir)
        os.makedirs(self.log_dir, exist_ok=True)
        # create log filename with timestamp
        log_filename = f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        log_filepath = os.path.join(self.log_dir, log_filename) 

        # configure logging settings
        logging.basicConfig(    
            filename=log_filepath,
            level=logging.INFO,
            format="[%(asctime)s] %(levelname)s: %(name)s (line:%(lineno)d)- %(message)s",  
        )
        

    def get_logger(self, name=__file__):
        return logging.getLogger(os.path.basename(name))

if __name__ == "__main__":
    logger=CustomLogger()
    logger.get_logger(__file__).info("This is an custom logger info message")
    