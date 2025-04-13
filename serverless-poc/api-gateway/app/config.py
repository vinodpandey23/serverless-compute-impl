import logging
import os

LOGS_DIR = os.environ["LOGS_DIR"]
FUNCTION_MANAGER_URL = os.environ["FUNCTION_MANAGER_URL"]
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(f"{LOGS_DIR}/api_gateway.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Docker compose specific values
# FUNCTION_MANAGER_URL = "http://function-manager:5000"
