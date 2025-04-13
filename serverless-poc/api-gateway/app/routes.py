import time

import httpx
from fastapi import APIRouter, HTTPException, UploadFile, File, Form

from config import FUNCTION_MANAGER_URL, logger
from models import ExecutionRequest

router = APIRouter()
# Persistent HTTP client
client = httpx.AsyncClient(timeout=10)


@router.get("/health")
async def health_check():
    return {"status": "ok"}


@router.post("/register")
async def register_function(function_name: str = Form(...),
                            file: UploadFile = File(...)):
    logger.info(f"Registering function: {function_name}")
    response = await client.post(
        url=f"{FUNCTION_MANAGER_URL}/register",
        files={"file": (file.filename, file.file, file.content_type)},
        data={"function_name": function_name}
    )

    if response.status_code != 200:
        logger.error(f"Failed to register function {function_name}: "
                     f"{response.status_code} {response.text}")
        raise HTTPException(status_code=response.status_code,
                            detail=response.text)

    logger.info(f"Function {function_name} registered successfully")
    return response.json()


@router.post("/execute")
async def execute_function(request: ExecutionRequest):
    logger.info(f"Executing function: {request.function_name}")
    start_time = time.time()
    response = await client.post(f"{FUNCTION_MANAGER_URL}/execute",
                                 json=request.dict())

    if response.status_code != 200:
        logger.error(f"Execution failed for function {request.function_name}: "
                     f"{response.status_code} {response.text}")
        raise HTTPException(status_code=response.status_code,
                            detail=response.text)

    total_time = time.time() - start_time
    logger.info(f"Function {request.function_name} executed in "
                f"{total_time:.4f} seconds")

    return response.json()
