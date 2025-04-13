from fastapi import APIRouter, HTTPException, UploadFile, File, Form

from cleanup_service import CleanupService
from config import logger
from execution_service import ExecutionService
from models import FunctionExecutionRequest
from registraction_service import RegistrationService

router = APIRouter()
cleanup_service = CleanupService()
registration_service = RegistrationService()
execution_service = ExecutionService(cleanup_service)


@router.get("/health")
async def health_check():
    return {"status": "ok"}


@router.post("/register")
async def register_function(function_name: str = Form(...),
                            file: UploadFile = File(...)):
    logger.info(f"Registering function: {function_name}")
    try:
        result = registration_service.register_function(function_name, file)
        return result
    except Exception as e:
        logger.error(f"Error registering function '{function_name}': {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/execute")
async def execute_function(request: FunctionExecutionRequest):
    logger.info(f"Executing function: {request.function_name} with "
                f"payload: {request.payload}")
    try:
        result = execution_service.execute_function(request.function_name,
                                                    request.payload)
        return result
    except Exception as e:
        logger.error(f"Error executing function '{request.function_name}': "
                     f"{e}")
        raise HTTPException(status_code=500, detail=str(e))
