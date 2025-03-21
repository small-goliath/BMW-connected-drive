import logging
from typing import Callable, Awaitable
from bimmer_connected.models import MyBMWRemoteServiceError
from fastapi import APIRouter
from app import bmw_account

router = APIRouter()

async def handle_remote_service(service_call: Callable[[], Awaitable]) -> str:
    try:
        result = await service_call()
        logging.info(f"{service_call.__name__} executed successfully: {result.details}")
        return str(result.details.get("eventStatus", "Unknown")).strip('"')
    except MyBMWRemoteServiceError as e:
        logging.error(f"BMW Remote Service Error: {e}")
        return "bmw에서 요청을 받지 않아."

@router.post("/doors", response_model=str)
async def lock_the_door() -> str:
    return await handle_remote_service(bmw_account.vehicle.remote_services.trigger_remote_door_lock)

@router.delete("/doors", response_model=str)
async def unlock_the_door() -> str:
    return await handle_remote_service(bmw_account.vehicle.remote_services.trigger_remote_door_unlock)

@router.post("/horn", response_model=str)
async def horn() -> str:
    return await handle_remote_service(bmw_account.vehicle.remote_services.trigger_remote_horn)

@router.post("/air-conditioning", response_model=str)
async def start_air_conditioning() -> str:
    return await handle_remote_service(bmw_account.vehicle.remote_services.trigger_remote_air_conditioning)

@router.delete("/air-conditioning", response_model=str)
async def stop_air_conditioning() -> str:
    return await handle_remote_service(bmw_account.vehicle.remote_services.trigger_remote_air_conditioning_stop)

@router.post("/charging", response_model=str)
async def start_charging() -> str:
    return await handle_remote_service(bmw_account.vehicle.remote_services.trigger_charge_start)

@router.delete("/charging", response_model=str)
async def stop_charging() -> str:
    return await handle_remote_service(bmw_account.vehicle.remote_services.trigger_charge_stop)

@router.patch("/charging", response_model=str)
async def update_charging_settings(target_soc: int) -> str:
    return await handle_remote_service(
        lambda: bmw_account.vehicle.remote_services.trigger_charging_settings_update(target_soc=target_soc)
    )

@router.post("/poi", response_model=str)
async def update_charging_settings(target: str) -> str:
    return await handle_remote_service(
        lambda: bmw_account.vehicle.remote_services.trigger_send_poi({"name": target})
    )