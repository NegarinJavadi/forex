import logging
import os
#This code is designed to create and manage log files for an application

LOG_FORMAT = "%(asctime)s %(message)s"
# Defines the format of the log messages. %(asctime)s will be replaced with the current date and time, 
# and %(message)s will be replaced with the actual log message
DEFAULT_LEVEL = logging.DEBUG
#Sets the default logging level to DEBUG. This means all messages at the DEBUG level and above will be logged

class LogWrapper:

    PATH = './logs'
    #A class attribute that specifies the directory where log files will be stored

    def __init__(self, name, mode="w"):
    #A class attribute that specifies the directory where log files will be stored
        self.create_directory()
        #create the logs directory if it doesn't exist
        self.filename = f"{LogWrapper.PATH}/{name}.log"
        #Sets the filename for the log file
        self.logger = logging.getLogger(name)
        #Creates a new logger with the given name
        self.logger.setLevel(DEFAULT_LEVEL)
        #Sets the logging level for this logger

        file_handler = logging.FileHandler(self.filename, mode=mode)
        #Creates a file handler that writes log messages to the specified file. 
        #The mode parameter determines whether the file is overwritten ("w") or appended ("a")
        formatter = logging.Formatter(LOG_FORMAT, datefmt='%Y-%m-%d %H:%M:%S')
        #Creates a formatter that formats the log messages according to LOG_FORMAT

        file_handler.setFormatter(formatter)
        #Sets the formatter for the file handler
        self.logger.addHandler(file_handler)
        #Adds the file handler to the logger

        self.logger.info(f"Logwrapper init() {self.filename}")
        #Logs an informational message indicating that the log wrapper has been initialized


    def create_directory(self):
    #create the logs directory if it doesn't already exist
        if not os.path.exists(LogWrapper.PATH):
            os.makedirs(LogWrapper.PATH)
            #Creates the directory