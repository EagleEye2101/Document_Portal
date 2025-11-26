import logging
import os
from datetime import datetime

class CustomLogger:
    def __init__(self,log_dir="logs"):
        # ensure logs directory exists
        self.logs_dir = os.path.join(os.getcwd(),log_dir)
        os.makedirs(self.logs_dir, exist_ok=True)
        # create log filename with timestamp
        log_file = f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        log_file_path = os.path.join(self.logs_dir, log_file) 

        # configure logging settings
        logging.basicConfig(    
            filename=log_file_path,
            format="[%(asctime)s] %(levelname)s %(name)s (line:%(lineno)d)- %(message)s",  
            level=logging.INFO,
        )
        # internal holder for a default logger instance so attribute
        # access on CustomLogger can be delegated when needed
        self._default_logger = None
    def get_logger(self, name=__file__):
        logger = logging.getLogger(os.path.basename(name))
        # keep a reference for delegation if someone uses the
        # CustomLogger instance directly (common mistake in notebooks)
        self._default_logger = logger
        return logger

    def __getattr__(self, item):
        """Delegate attribute access to the underlying logger when
        possible. This makes `CustomLogger()` behave like a
        `logging.Logger` for convenience and prevents
        AttributeError: 'CustomLogger' object has no attribute 'log'."""
        if self._default_logger is not None:
            return getattr(self._default_logger, item)
        raise AttributeError(f"{self.__class__.__name__!r} object has no attribute {item!r}")

if __name__ == "__main__":
    logger=CustomLogger()
    logger=logger.get_logger(__file__)
    logger.info("This is an custom logger info message")
    

# # ---- Alternative Implementation to write it to console logs ----- #
# import logging
# import os
# from datetime import datetime

# class CustomLogger:
#     def __init__(self, log_dir="logs"):
#         self.logs_dir = os.path.join(os.getcwd(), log_dir)
#         os.makedirs(self.logs_dir, exist_ok=True)
#         log_file = f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
#         self.log_file_path = os.path.join(self.logs_dir, log_file)

#     def get_logger(self, name=__file__):
#         """ 
#         Returns a logger instance with file+ console handlers.
#         Default name is the current filename (without path).
#         """
#         logger_name = os.path.basename(name)
#         logger = logging.getLogger(logger_name)
#         logger.setLevel(logging.INFO)

#         # Formatter for both handlers
#         file_formatter = logging.Formatter(
#             "[%(asctime)s] %(levelname)s %(name)s (line:%(lineno)d)- %(message)s"
#         )
#         console_formatter = logging.Formatter("[ %(levelname)s ] %(message)s")    
#         # File handler (logs saved to file) 
#         file_handler = logging.FileHandler(self.log_file_path)
#         file_handler.setFormatter(file_formatter)

#         #console handler (logs printed to console/terminal)
#         console_handler = logging.StreamHandler()
#         console_handler.setFormatter(console_formatter)

#         # Avoid duplicate handlers if logger already has them
#         # NOTE: use the callable `hasHandlers()` not the method object `hasHandlers`
#         if not logger.hasHandlers():
#             logger.addHandler(file_handler)
#             logger.addHandler(console_handler)
        
#         return logger
    
# #-----Usage Example -----#
# if __name__ == "__main__":
#     logger = CustomLogger().get_logger(__file__) #logger will use filename as name
#     logger.info("Logger initialized successfiully.")
