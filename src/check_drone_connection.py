import asyncio
from mavsdk import System

import sys

async def run():
    """Checks if the drone controller is connected
    and recognised properly by the Jetson Nano."""

    drone = System()

    try:
        await asyncio.wait_for(drone.connect(system_address='serial:///dev/ttyTHS1:57600'), timeout=5)
    except asyncio.TimeoutError:
        print("ERROR: No se pudo conectar al dron dentro del tiempo especificado")
        return


    async for state in drone.core.connection_state():
        if state.is_connected:
            print("¡Dron encontrado!")
            break

    

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())