import logging
from bimmer_connected.vehicle.fuel_and_battery import ChargingState
from bimmer_connected.vehicle.doors_windows import LockState
from fastapi import APIRouter, HTTPException
from app import bmw_account

router = APIRouter()

CHARGING_STATUS_MAP = {
    ChargingState.CHARGING: "충전 중입니다.",
    ChargingState.COMPLETE: "충전이 완료되었습니다.",
    ChargingState.ERROR: "충전 중 오류가 발생했습니다.",
    ChargingState.FINISHED_FULLY_CHARGED: "배터리가 완전히 충전되었습니다.",
    ChargingState.FINISHED_NOT_FULL: "충전이 완료되었지만 배터리가 가득 차지는 않았습니다.",
    ChargingState.NOT_CHARGING: "충전 중이지 않습니다.",
    ChargingState.FULLY_CHARGED: "배터리가 가득 찼습니다.",
    ChargingState.INVALID: "충전 상태가 올바르지 않습니다.",
    ChargingState.PLUGGED_IN: "충전기가 연결되어 있습니다.",
    ChargingState.WAITING_FOR_CHARGING: "충전을 기다리고 있습니다.",
    ChargingState.TARGET_REACHED: "충전 목표에 도달했습니다.",
    ChargingState.UNKNOWN: "충전 상태를 알 수 없습니다."
}

DOORS_STATUS_MAP = {
    LockState.LOCKED: "모든 문이 잠겨 있습니다.",
    LockState.SECURED: "모든 문이 잠겨 있습니다.",
    LockState.SELECTIVE_LOCKED: "특정 문이 잠겨 있지 않습니다.",
    LockState.PARTIALLY_LOCKED: "특정 문이 잠겨 있지 않습니다.",
    LockState.UNLOCKED: "모든 문이 잠겨 있지 않습니다.",
    LockState.UNKNOWN: "문 상태를 알 수 없습니다."
}

async def update_vehicle_state():
    try:
        await bmw_account.vehicle.get_vehicle_state()
    except Exception as e:
        logging.error(f"차량 상태를 갱신하는 중 오류가 발생했습니다: {str(e)}");
        raise HTTPException(status_code=500, detail=f"차량 상태를 갱신하는 중 오류가 발생했습니다.")

@router.get("/charging", response_model=str)
async def search_charging_status() -> str:
    await update_vehicle_state()

    charging_status = bmw_account.vehicle.fuel_and_battery.charging_status
    charging_message = CHARGING_STATUS_MAP.get(charging_status, "충전 상태를 알 수 없습니다.")
    target_percent = bmw_account.vehicle.fuel_and_battery.charging_target

    return f"충전 목표치는 {target_percent}%이며, 현재 충전 상태는 {charging_message}"


@router.get("/doors-windows", response_model=str)
async def search_doors_and_windows_status() -> str:
    await update_vehicle_state()

    door_lock_state = bmw_account.vehicle.doors_and_windows.door_lock_state
    door_message = DOORS_STATUS_MAP.get(door_lock_state, "문의 상태를 알 수 없습니다.")

    are_windows_closed = bmw_account.vehicle.doors_and_windows.all_windows_closed
    window_message = "모든 창문과 선루프가 닫혀 있으며" if are_windows_closed else "창문 또는 선루프가 열려 있으며"

    return f"{window_message} 차량의 문 상태는 {door_message}"
