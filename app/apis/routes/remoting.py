import logging
from bimmer_connected.models import MyBMWRemoteServiceError
from fastapi import APIRouter
from app import bmw_account

router = APIRouter()

@router.post("/doors", response_model = str)
async def lock_the_door() -> str:
    try:
        result = await bmw_account.vehicle.remote_services.trigger_remote_door_lock()
        logging.debug(f"result: {result.details}")
        return str(result.details.get('eventStatus')).strip('"')
    except MyBMWRemoteServiceError as e:
        return "bmw에서 요청을 받지 않아."


@router.delete("/doors", response_model = str)
async def unlock_the_door() -> str:
    try:
        result = await bmw_account.vehicle.remote_services.trigger_remote_door_unlock()
        logging.debug(f"result: {result.details}")
        return str(result.details.get('eventStatus')).strip('"')
    except MyBMWRemoteServiceError as e:
        return "bmw에서 요청을 받지 않아."
    
@router.post("/horn", response_model = str)
async def horn() -> str:
    try:
        result = await bmw_account.vehicle.remote_services.trigger_remote_horn()
        logging.debug(f"result: {result.details}")
        return str(result.details.get('eventStatus')).strip('"')
    except MyBMWRemoteServiceError as e:
        return "bmw에서 요청을 받지 않아."
    
@router.post("/air-conditioning", response_model = str)
async def start_air_conditioning() -> str:
    try:
        result = await bmw_account.vehicle.remote_services.trigger_remote_air_conditioning()
        logging.debug(f"result: {result.details}")
        return str(result.details.get('eventStatus')).strip('"')
    except MyBMWRemoteServiceError as e:
        return "bmw에서 요청을 받지 않아."
    
@router.delete("/air-conditioning", response_model = str)
async def stop_air_conditioning() -> str:
    try:
        result = await bmw_account.vehicle.remote_services.trigger_remote_air_conditioning_stop()
        logging.debug(f"result: {result.details}")
        return str(result.details.get('eventStatus')).strip('"')
    except MyBMWRemoteServiceError as e:
        return "bmw에서 요청을 받지 않아."

@router.post("/charging", response_model = str)
async def start_charging() -> str:
    try:
        result = await bmw_account.vehicle.remote_services.trigger_charge_start()
        logging.debug(f"result: {result.details}")
        return str(result.details.get('eventStatus')).strip('"')
    except MyBMWRemoteServiceError as e:
        return "bmw에서 요청을 받지 않아."

@router.delete("/charging", response_model = str)
async def stop_charging() -> str:
    try:
        result = await bmw_account.vehicle.remote_services.trigger_charge_stop()
        logging.debug(f"result: {result.details}")
        return str(result.details.get('eventStatus')).strip('"')
    except MyBMWRemoteServiceError as e:
        return "bmw에서 요청을 받지 않아."