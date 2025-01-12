from bimmer_connected.vehicle.fuel_and_battery import ChargingState
from bimmer_connected.vehicle.doors_windows import LockState
from fastapi import APIRouter
from app import bmw_account

router = APIRouter()

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

doorsStatusMap = {
    LockState.LOCKED: "모든 문이 잠겨있어.",
    LockState.SECURED: "모든 문이 잠겨있어.",
    LockState.SELECTIVE_LOCKED: "특정 문이 잠겨있지 않아.",
    LockState.PARTIALLY_LOCKED: "특정 문이 잠겨있지 않아.",
    LockState.UNLOCKED: "모든 문이 잠겨있지 않아.",
    LockState.UNKNOWN: "문의 상태를 알 수 없어."
}
    
@router.get("/charging", response_model=str)
async def lock_the_door() -> str:
    await bmw_account.vehicle.get_vehicle_state()

    status = bmw_account.vehicle.fuel_and_battery.charging_status
    status = chargingStatusMap.get(status, "알 수 없어.")

    target_percent = bmw_account.vehicle.fuel_and_battery.charging_target

    return f"목표치는 {target_percent} 퍼센트이고 지금 충전 상태는 {status}"


@router.get("/doors-windows", response_model=str)
async def lock_the_door() -> str:
    await bmw_account.vehicle.get_vehicle_state()

    doors_status = bmw_account.vehicle.doors_and_windows.door_lock_state
    doors_status = doorsStatusMap.get(doors_status, "문의 상태를 알 수 없어.")

    is_close_windows = await bmw_account.vehicle.doors_and_windows.all_windows_closed()
    windows_status = "창문과 선루프가 닫혀있고" if is_close_windows else "창문 혹은 선루프가 열려있고"

    return f"{windows_status} 차량의 {doors_status}"

