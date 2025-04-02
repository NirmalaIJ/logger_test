import logging
import os


class CustomFormatter(logging.Formatter):
    """ Custom Formatter does these 2 things:
    1. Overrides 'funcName' with the value of 'func_name_override', if it exists.
    2. Overrides 'filename' with the value of 'file_name_override', if it exists.
    """
    grey = '\x1b[38;21m'
    blue = '\x1b[38;5;39m'
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'

    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: self.grey + self.fmt + self.reset,
            logging.INFO: self.blue + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset
        }
    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

class CustomFormatterFile(logging.Formatter):
    """ Custom Formatter does these 2 things:
    1. Overrides 'funcName' with the value of 'func_name_override', if it exists.
    2. Overrides 'filename' with the value of 'file_name_override', if it exists.
    """
    def format(self, record):
        if hasattr(record, 'func_name_override'):
            record.funcName = record.func_name_override
        if hasattr(record, 'file_name_override'):
            record.filename = record.file_name_override

        return super(CustomFormatterFile, self).format(record)

def get_logger(log_file_name, log_sub_dir=""):
    """ Creates a Log File and returns Logger object """

    windows_log_dir = r'D:\Documents\Python_ex\logger_test'
    linux_log_dir = '/logs_dir/'

    # Build Log file directory, based on the OS and supplied input
    log_dir = windows_log_dir if os.name == 'nt' else linux_log_dir
    log_dir = os.path.join(log_dir, log_sub_dir)

    # Create Log file directory if not exists
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Build Log File Full Path
    logPath = log_file_name if os.path.exists(log_file_name) else os.path.join(log_dir, (str(log_file_name) + '.log'))

    # Define format for logs
    fmt = '%(asctime)s - %(levelname)-10s - %(filename)s - %(funcName)s - %(message)s'

    # Create logger object and set the format for logging and other attributes
    logger = logging.Logger(log_file_name)
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(logPath, 'a+')
    """ Set the formatter of 'CustomFormatter' type as we need to log base function name and base file name """
    handler.setFormatter(CustomFormatterFile(fmt))
    logger.addHandler(handler)

    # Create stdout handler for logging to the console (logs all five levels)
    stdout_handler = logging.StreamHandler()
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(CustomFormatter(fmt))

    # Add both handlers to the logger
    logger.addHandler(stdout_handler)

    # Return logger object
    return logger
