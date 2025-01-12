import logging
from typing import Callable, Awaitable
from bimmer_connected.models import MyBMWRemoteServiceError
from bimmer_connected.vehicle.fuel_and_battery import ChargingState
from fastapi import APIRouter
from app import bmw_account

router = APIRouter()

# TODO: 차량 각종 상태 조회

chargingStatusMap = {
    ChargingState.CHARGING: "충전 중이야.",
    ChargingState.COMPLETE: "충전 완료했어.",
    ChargingState.ERROR: "충전 오류가 났어.",
    ChargingState.FINISHED_FULLY_CHARGED: "전기가 가득찼어.",
    ChargingState.FINISHED_NOT_FULL: "충전은 끝났지만 전기가 가득차지 않았어.",
    ChargingState.NOT_CHARGING: "충전중이지 않아.",
    ChargingState.FULLY_CHARGED: "전기가 가득찼어.",
    ChargingState.INVALID: "충전 상태가 이상해.",
    ChargingState.PLUGGED_IN: "충전기가 꽂아져있어.",
    ChargingState.WAITING_FOR_CHARGING: "충전 대기 중이야.",
    ChargingState.TARGET_REACHED: "충전 목표치에 도달했어.",
    ChargingState.UNKNOWN: "알 수 없어."
    }
    
@router.get("/", response_model=str)
async def lock_the_door() -> str:
    await bmw_account.vehicle.get_vehicle_state()

    status = await bmw_account.vehicle.fuel_and_battery.charging_status
    status = chargingStatusMap.get(status, "알 수 없어.")

    target_percent = bmw_account.vehicle.fuel_and_battery.charging_target

    return f"목표치는 {target_percent} 퍼센트이고 지금 충전 상태는 {status}"
