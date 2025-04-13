import uvicorn
from fastapi import FastAPI

from config import logger
from routes import router

app = FastAPI()
app.include_router(router)

logger.info("Function Manager initialized and router included.")

if __name__ == "__main__":
    logger.info("Starting Function Manager...")
    uvicorn.run("function_manager:app", host="localhost", port=5000)
    logger.info("Function Manager stopped.")
