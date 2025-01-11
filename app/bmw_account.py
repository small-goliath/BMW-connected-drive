import logging
import sys
from typing import Optional

from bimmer_connected.account import MyBMWAccount
from bimmer_connected.const import Regions
from bimmer_connected.vehicle.vehicle import MyBMWVehicle
from app.core.config import settings

vehicle: Optional[MyBMWVehicle]

async def initialize_vehicle():
    global vehicle
    
    logging.info("Initializing vehicle...")
    account = MyBMWAccount(settings.USERNAME, settings.PASSWORD, Regions.REST_OF_WORLD, hcaptcha_token=settings.CAPCHA_TOKEN)
    await account.get_vehicles()
    vehicle = account.get_vehicle(settings.VIN_NUMBER)
    if vehicle is None:
        logging.error("vehicle is required!!!")
        sys.exit(0)
    else:
        logging.debug(f"Vehicle initialized: {vehicle.brand} {vehicle.name}")