import uvicorn
from fastapi import FastAPI

from config import logger
from routes import router

app = FastAPI()
app.include_router(router)

logger.info("API Gateway initialized and router included.")

if __name__ == "__main__":
    logger.info("Starting API Gateway...")
    uvicorn.run("api_gateway:app", host="localhost", port=8000)
    logger.info("API Gateway stopped.")
