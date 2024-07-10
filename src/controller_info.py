import os

import getpass

def run_drone_connection_checker():
    """Executes the program "check_drone_connection.py"
    ensuring it can access the drone controller properly.
    
    Returns:
        html: A string with the output message of the program."""

    WWWDATA_PASSWORD = # WRITE THE PASSWORD YOU SET FOR THE USER WWW-DATA
    
    PYTHON_INTERPRETER = '/opt/flask-app/flask-venv/bin/python3.7'
    PROGRAM_ROUTE = '/opt/flask-app/src/check_drone_connection.py'

    program = (f'echo \'{WWWDATA_PASSWORD}\' | '
               f'sudo -S {PYTHON_INTERPRETER} {PROGRAM_ROUTE}')
    
    # Executes the program
    output = os.popen(program).read()

    html = '\n' \
            '\n' \
            +output+ \
            '\n' \
            '\n'
    return [html]
    
        
