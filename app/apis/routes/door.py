import logging
from bimmer_connected.models import MyBMWRemoteServiceError
from fastapi import APIRouter
from app import bmw_account
import json


router = APIRouter()

@router.post("/", response_model = str)
async def open_the_door() -> str:
    try:
        result = await bmw_account.vehicle.remote_services.trigger_remote_door_lock()
        logging.debug(f"result: {result.details}")
        return result.details.get('eventStatus')
    except MyBMWRemoteServiceError as e:
        return "bmw에서 요청을 받지 않아."


@router.delete("/", response_model = str)
async def close_the_door() -> str:
    try:
        result = await bmw_account.vehicle.remote_services.trigger_remote_door_unlock()
        logging.debug(f"result: {result.details}")
        return result.details.get('eventStatus')
    except MyBMWRemoteServiceError as e:
        return "bmw에서 요청을 받지 않아."