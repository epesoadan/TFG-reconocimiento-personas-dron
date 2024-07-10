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
logging.basicConfig(filename=LOG_FILE, level=logging.INFO) # Switch "INFO" for "DEBUG" for more program information

# Cleaning previous captures
programa = f'rm {FOUND_PEOPLE_FOLDER_PATH}*'
os.popen(programa).read()
with open(COORDINATES_FILE_PATH, 'w') as archivo:
    pass
os.chdir(FOUND_PEOPLE_FOLDER_PATH)
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
        # (Doesn't wait for the attributes to be ready, so it connects faster.
        # Might make the program pause later down the line if it tries to access an
        # attribute that isn't ready yet.)
        drone = connect('udp:127.0.0.1:14550', baud=57600, wait_ready=True, timeout=50)
    except Exception as e:
        logging.error("TIMEOUT: Couldn't connect with drone in 50 seconds.")
        return
    elapsed_time = time.time() - start_time


    if drone is not None:
        logging.info("Drone found!\n")
        logging.debug(f"Elapsed time: {elapsed_time} s")
    else:
        logging.error("Couldn't connect to drone, but no exception was caught.")
        return
    return drone

def detect_people(drone, current_flight_mode):
    """Detects people in the camera's video feed and
    saves the image. It also calls the function
    "get_drone_coordinates" to get the coordinates
    of the location where the person was found.
    
    Args:
        drone: The variable representing the drone
        current_flight_mode: The drone's current flight mode"""

    img = camera.Capture()
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
                get_drone_coordinates(drone)
                # Orbits in its current position, unless it's in RTL mode
                if (current_flight_mode != "RTL"):
                    orbit(drone)
    
    logging.debug("------------------------")
    return

def get_drone_coordinates(drone):
    """Makes the drone loiter in its current position
    and accesses the drone's GPS to get its current coordinates.
    Also makes it orbit around its current position.
    
    Args:
        drone: The variable that represents the drone"""

    if (drone.gps_0.fix_type > 1): # If the GPS is working correctly
        location = drone.location.global_frame

        latitude = location.lat
        longitude = location.lon
        location_str = f"{latitude}, {longitude}"

        logging.info(f"Ubication: Latitude={latitude}, Longitude={longitude}\n")
        with open(COORDINATES_FILE_PATH, "a") as file:
            file.write(location_str + "\n")
    else:
        logging.error("The GPS is not working properly. Coordinates cannot be acquired.\n")
        with open(COORDINATES_FILE_PATH, "a") as file:
            file.write("No se pudo acceder al GPS\n")

    return

def orbit(drone):
    """Makes the drone orbit around its current position
    in a radius of 10 meters.
    
    Args:
        drone: The variable that represents the drone"""

    logging.info("The program will now take photos of the environment.\n\
    Switch to AUTO mode to continue with the mission, or RTL to finish it.")

    drone.parameters['CIRCLE_RADIUS'] = 10
    drone.parameters['CIRCLE_OPTIONS'] = 4 # Tells the drone to use its current position
                                           # as the center of the circle 
    drone.mode = VehicleMode("CIRCLE")
    return

def take_photo(drone):
    """Takes a photo and gets its current coordinates as well.
    
    Args:
        drone: The variable that represents the drone"""

    img = camera.Capture()
    if img is None:
        return
    logging.info("Took photo of the environment")
    detections = net.Detect(img)
    output.Render(img)
    get_drone_coordinates(drone)
    return

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
            # The same happens if it's in RTL mode, but it won't circle after detecting a person
            if (current_flight_mode == "AUTO" or current_flight_mode == "RTL"):
                detect_people(drone, current_flight_mode)
            # If the drone is on CIRCLE mode, it means it's orbiting around a person
            # it found, so it starts taking photos every 3 seconds
            elif (current_flight_mode == "CIRCLE"):
                take_photo(drone)
                time.sleep(3)
            # If the drone is in any other mode, doesn't do anything
        except Exception as e:
            logging.error(f"{type(e).__name__} - {str(e)}")
            return

if __name__ == "__main__":
    main()