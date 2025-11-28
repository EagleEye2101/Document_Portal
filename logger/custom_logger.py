import logging
import os
from datetime import datetime

# Optional dependency: structlog. If it's not available, fall back to stdlib logging
try:
    import structlog
    _HAS_STRUCTLOG = True
except Exception:
    structlog = None
    _HAS_STRUCTLOG = False

class CustomLogger:
    def __init__(self,log_dir="logs"):
        # ensure logs directory exists
        self.logs_dir = os.path.join(os.getcwd(),log_dir)
        os.makedirs(self.logs_dir, exist_ok=True)
        # create log filename with timestamp
        log_file = f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        self.log_file_path = os.path.join(self.logs_dir, log_file) 

        # # configure logging settings
        # logging.basicConfig(    
        #     filename=log_file_path,
        #     format="[%(asctime)s] %(levelname)s %(name)s (line:%(lineno)d)- %(message)s",  
        #     level=logging.INFO,
        #)
        # internal holder for a default logger instance so attribute
        # access on CustomLogger can be delegated when needed
        #self._default_logger = None
    def get_logger(self, name=__file__):
        logger_name = os.path.basename(name)

        # Configure logging for console + file (both JSON)
        file_handler = logging.FileHandler(self.log_file_path)
        file_handler.setLevel(logging.INFO)
        # Fix: use proper format specifier `%(message)s` so Formatter doesn't raise
        file_handler.setFormatter(logging.Formatter("%(message)s")) # Raw JSON lines

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter("%(message)s")) # Raw JSON lines

        logging.basicConfig(
            level=logging.INFO,
            format="%(message)s",  # Raw JSON lines
            handlers=[console_handler, file_handler]
        )

        # Configure structlog for JSON structured logging if available
        if _HAS_STRUCTLOG:
            try:
                structlog.configure(
                    processors=[
                        structlog.processors.TimeStamper(fmt="iso", utc=True, key="timestamp"),
                        structlog.processors.add_log_level,
                        structlog.processors.EventRenamer(to="event"),
                        structlog.processors.JSONRenderer()
                    ],
                    logger_factory=structlog.stdlib.LoggerFactory(),
                    cache_logger_on_first_use=True,
                )
                return structlog.get_logger(logger_name)
            except Exception:
                # If structlog fails to configure for any reason, fall back
                # to the standard library logger so logs still appear in file.
                return logging.getLogger(logger_name)
        else:
            # Fallback: return a standard library logger instance
            return logging.getLogger(logger_name)
#------Usage Example -----#
if __name__ == "__main__":
    logger = CustomLogger().get_logger(__file__) #logger will use filename as name
    logger.info("User uploaded a file ", user_id=123, filename="sample.pdf")
    logger.error("Failed to process PDF file", error="File not found", user_id=123)
    

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
