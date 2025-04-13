import logging
import os

import docker
from cachetools import TTLCache

FUNCTIONS_DIR = os.environ["FUNCTIONS_DIR"]
LOGS_DIR = os.environ["LOGS_DIR"]
WARM_UP_TIME = float(os.environ["WARM_UP_TIME"])

cached_errors = TTLCache(maxsize=100, ttl=WARM_UP_TIME)
cached_containers = TTLCache(maxsize=100, ttl=WARM_UP_TIME)
docker_client = docker.from_env()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(f"{LOGS_DIR}/function_manager.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
