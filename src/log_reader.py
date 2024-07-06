import os
import time

def read_log_file():
    """Reads the contents of the log file.
    
    Returns:
        log_content: A string with the content of the log file.
        error_message: A string with the exception found
            if there was an issue accessing the file."""

    try:
        with open('/opt/flask-app/logs/programlog.log', 'r') as log_file:
            log_content = log_file.read()
        return log_content
    except Exception as e:
        error_message = str(e)
        return error_message