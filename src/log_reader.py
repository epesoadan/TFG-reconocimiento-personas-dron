import os
import time

def read_log_file():
    """Reads the contents of the log file.
    
    Returns:
        log_content: A string with the last 33 lines of the log file.
        error_message: A string with the exception found
            if there was an issue accessing the file."""
    
    try:
        with open('/opt/flask-app/logs/programlog.log', 'r') as log_file:
            
            lines = log_file.readlines()
            # Get the last 33 lines (or all lines if less than 33)
            last_lines = lines[-33:]
            log_content = ''.join(last_lines)
            
            return log_content
    except Exception as e:
        error_message = str(e)
        return error_message