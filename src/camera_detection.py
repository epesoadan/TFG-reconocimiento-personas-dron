from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput
import sys
import time
import os
import asyncio

from mavsdk import System
from mavsdk.telemetry import FlightMode
from mavsdk.action import OrbitYawBehavior

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
logging.info("Output folder set")

async def connect_to_drone(drone):
    """Checks the connection with the drone.
    
    Args:
        drone: The variable that stores the drone's information."""

    logging.info("Connecting with drone...")

    try:
        await asyncio.wait_for(drone.connect(system_address='udp://:14550'), timeout=5)
    except asyncio.TimeoutError:
        logging.info("TIMEOUT ERROR: Couldn't connect with drone in 5 seconds.")
        return

    async for state in drone.core.connection_state():
        if state.is_connected:
            logging.info("Drone found")
            break

async def detect_people(drone):
    """Detects people in the camera's video feed and
    saves the image. It also calls the function
    "get_drone_coordinates" to get the coordinates
    of the location where the person was found."""

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
                start_time = time.time()
                await get_drone_coordinates(drone)
                elapsed_time = time.time() - start_time
                logging.info(f'Elapsed time: {elapsed_time} s')
    
    logging.debug("------------------------")

async def get_drone_coordinates(drone):
    """Makes the drone loiter in its current position
    and accesses the drone's GPS to get its current coordinates."""

    logging.info("Waiting for drone to have a global position estimate...")
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

    logging.debug(f"Ubicación: Latitud={latitude}, Longitud={longitude}")

    with open(COORDINATES_FILE_PATH, "a") as file:
        file.write(location_str + "\n")
            
    yaw_behavior = OrbitYawBehavior.HOLD_FRONT_TO_CIRCLE_CENTER


    logging.debug('Do orbit at 10m height from the ground')
    await drone.action.do_orbit(radius_m=10,
                                velocity_ms=2,
                                yaw_behavior=yaw_behavior,
                                latitude_deg=position.latitude_deg,
                                longitude_deg=position.longitude_deg,
                                absolute_altitude_m=orbit_height)
    return

async def get_flight_mode(drone):
    async for flight_mode in drone.telemetry.flight_mode():
        return flight_mode

async def main():
    drone = System()
    await connect_to_drone(drone)

    logging.info("Recognition program started")
    while True:
        try:
            current_flight_mode = await get_flight_mode(drone)
            # If the drone is on AUTO mode (called MISSION in mavsdk),
            # it starts detecting people
            if current_flight_mode == FlightMode.MISSION:
                logging.debug("Drone is in AUTO mode, starting people detection.")
                await detect_people(drone)
            # If the drone is in any other mode
            else:
                logging.info(f"Drone is in {current_flight_mode} mode, waiting...")
        except asyncio.TimeoutError:
            logging.error("Timeout while fetching flight mode.")
        except Exception as e:
            logging.error(f"Error in main: {type(e).__name__} - {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())