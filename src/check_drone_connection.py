from dronekit import connect, VehicleMode

import sys
import time

def run():
    """Checks if the drone controller is connected
    and recognised properly by the Jetson Nano."""

    start_time = time.time()
    try:
        # Turn wait_ready to False if you want it to connect to the drone
        # without waiting for its attributes to be ready
        drone = connect('/dev/ttyTHS1', baud=57600, wait_ready=True, timeout=50)
    except Exception as e:
        print(f"ERROR: {e}")
        return
    elapsed_time = time.time() - start_time

    if drone is not None:
        print("¡Dron encontrado!")
        print(f"Tiempo transcurrido: {elapsed_time} s")
    else:
        print("ERROR: No se pudo conectar al dron dentro del tiempo especificado, pero no saltó ninguna excepción")

    drone.close()
    return

    

if __name__ == "__main__":
    run()