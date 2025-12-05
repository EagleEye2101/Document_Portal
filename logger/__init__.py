from logger.custom_logger import CustomLogger

# Create a global logger instance
_logger_instance = CustomLogger()
GLOBAL_LOGGER = _logger_instance.get_logger(__name__)

__all__ = ["GLOBAL_LOGGER", "CustomLogger"]
