import os
import signal

def manage_process():
    """Stops the camera_detection program.
    
    Returns:
        A string indicating if the program was stopped correctly or not."""

    WWWDATA_PASSWORD = 'dr0neproject' # Change the password to the one you set for the user www-data

    program_to_stop = 'pgrep -f camera_detection.py'
    
    # Accessing the PID of the camera_detection program
    pid = os.popen(program_to_stop).read()
    pids_list = pid.split()

    # Verifying if there's at least 3 PIDs, given that properly
    # executing camera_detection.py through the graphical interface
    # uses three commands.
    if len(pids_list) >= 3:
        # The third PID is the one that corresponds to camera_detection.py
        program_to_stop = f'echo \'{WWWDATA_PASSWORD}\' | sudo -S kill ' + pids_list[2]
        os.popen(program_to_stop).read()
        return 'Escaneo detenido correctamente'
    return 'No se ha iniciado el escaneo'



    
    


