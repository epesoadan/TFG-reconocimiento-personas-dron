import os
# import json 

def run_execute_program():
    """Executes the program "camera_detection.py"
    properly, ensuring it can access the drivers
    connected to the Jetson Nano.
    
    Returns:
        output: A string with the output message of the program."""

    WWWDATA_PASSWORD = 'dr0neproject' # Change the password to the one you set for the user www-data
    PYTHON_INTERPRETER = '/opt/flask-app/flask-venv/bin/python3.7'
    PROGRAM_ROUTE = '/opt/flask-app/src/camera_detection.py'

    program = (f'echo \'{WWWDATA_PASSWORD}\' | '
               f'sudo -S {PYTHON_INTERPRETER} {PROGRAM_ROUTE}')

    # Executes the program
    output = os.popen(program).read()
    return output