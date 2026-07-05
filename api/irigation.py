from fastapi import APIRouter
from schemas.irigation import SoilData
from services.irigation import IrigationClass
router = APIRouter()

@router.post("/send-values")
async def send_values (values: SoilData):
    obj = IrigationClass(values)
    pump = await obj.check_temp()
    return pump