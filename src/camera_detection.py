from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput
import sys
import time
import os

from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil

import logging

FOUND_PEOPLE_FOLDER_PATH = "/opt/flask-app/found_people_captures/"
COORDINATES_FILE_PATH = "/opt/flask-app/coordenadas.txt"

# Starting the logging of the program
LOG_FILE = '/opt/flask-app/logs/programlog.log'
with open(LOG_FILE, 'w') as file:
    pass
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG) # Switch "INFO" for "DEBUG" for more program information

# Cleaning previous captures
programa = f'rm {FOUND_PEOPLE_FOLDER_PATH}*'
os.popen(programa).read()
with open(COORDINATES_FILE_PATH, 'w') as archivo:
    pass
logging.info("Previous captures cleaned")

# Loading the net that detects people
logging.info("Loading net...")
net = detectNet("ssd-mobilenet-v2", threshold=0.5)
logging.info("Net loaded successfully")

# Accessing camera
camera = videoSource("/dev/video0")
logging.info("Camera accesed successfully")

# Setting the output folder where the photos with people detected will go
output = videoOutput(FOUND_PEOPLE_FOLDER_PATH)
logging.info("Output folder set\n")

def connect_to_drone():
    """Checks the connection with the drone.
    It waits until all its attributes are ready.
    
    Returns:
        A variable that represents the drone"""

    logging.info("Connecting with drone...")

    start_time = time.time()
    try:
        # Turn wait_ready to False for debugging
        # (doesn't wait for the attributes to be ready, so it connects faster)
        drone = connect('udp:127.0.0.1:14550', baud=57600, wait_ready=True, timeout=50)
    except Exception as e:
        logging.info("TIMEOUT ERROR: Couldn't connect with drone in 50 seconds.")
        return
    elapsed_time = time.time() - start_time


    if drone is not None:
        logging.info("Drone found!\n")
        logging.debug(f"Elapsed time: {elapsed_time} s")
    else:
        logging.info("ERROR: Couldn't connect to drone, but no exception was caught.")
        return
    return drone

#async def detect_people(drone, current_flight_mode):
"""Detects people in the camera's video feed and
saves the image. It also calls the function
"get_drone_coordinates" to get the coordinates
of the location where the person was found."""

"""    img = camera.Capture()
    if img is None: # Capture timeout
        return

    detections = net.Detect(img)
    if detections:
        for info in detections:
            if info.ClassID == 1:
                logging.info("PERSON DETECTED")
                # Rendering the image
                output.Render(img)
                # Getting the coordinates
                start_time = time.time()
                await get_drone_coordinates(drone, current_flight_mode)
                elapsed_time = time.time() - start_time
                logging.info(f'Elapsed time: {elapsed_time} s')
    
    logging.debug("------------------------")"""

#async def get_drone_coordinates(drone, current_flight_mode):
"""Makes the drone loiter in its current position
and accesses the drone's GPS to get its current coordinates."""

"""    logging.info("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            logging.info("-- Global position estimate OK")
            break
        else:
            logging.info("-- ERROR: GPS couldn't be accessed")
            with open(COORDINATES_FILE_PATH, "a") as file:
                file.write("No se pudo acceder al GPS\n")
            return
    

    async for position in drone.telemetry.position():
        orbit_height = position.absolute_altitude_m + 10
        break

    latitude = position.latitude_deg
    longitude = position.longitude_deg
    location_str = f"{latitude}, {longitude}"

    logging.info(f"Ubication: Latitude={latitude}, Longitude={longitude}")

    with open(COORDINATES_FILE_PATH, "a") as file:
        file.write(location_str + "\n")
    
    # Starts orbiting around its current position
    # if not in RTL mode.
    if (current_flight_mode != FlightMode.RETURN_TO_LAUNCH):
        yaw_behavior = OrbitYawBehavior.HOLD_FRONT_TO_CIRCLE_CENTER


        logging.info('Orbiting in a 10m radius from the ground')
        await drone.action.do_orbit(radius_m=10,
                                    velocity_ms=2,
                                    yaw_behavior=yaw_behavior,
                                    latitude_deg=position.latitude_deg,
                                    longitude_deg=position.longitude_deg,
                                    absolute_altitude_m=orbit_height)
    return"""

def get_flight_mode(drone, previous_mode):
    """Returns the current flight mode.
    If the previous flight mode was different,
    it writes a message on the log.
    
    Args:
        drone: The variable that represents the drone
        previous_mode: The previous flight mode
        
    Returns:
        The current flight mode"""

    if (previous_mode != drone.mode.name):
        logging.info(f"CURRENT MODE: {drone.mode.name}")
    return drone.mode.name

def main():
    """The main function of the program."""

    current_flight_mode = "NONE"

    drone = connect_to_drone()
    if drone is None:
        return

    logging.info("Recognition program started")
    while True:
        try:
            current_flight_mode = get_flight_mode(drone, current_flight_mode)
            # If the drone is on AUTO mode, it starts detecting people
            # The same happens if it's in RTL mode, but it won't circle
            # after detecting a person
            if (current_flight_mode == "AUTO" or current_flight_mode == "RTL"):
                #detect_people(drone, current_flight_mode)
                logging.debug("test")
                time.sleep(1)
            # If the drone is in any other mode, doesn't do anything
        except asyncio.TimeoutError:
            logging.error("Timeout while fetching flight mode.")
        except Exception as e:
            logging.error(f"Error in main: {type(e).__name__} - {str(e)}")
            return

if __name__ == "__main__":
    main()