import threading
import time

from config import cached_containers, logger


class CleanupService:
    def __init__(self):
        logger.info("Initializing Execution Service")
        self._start_cleanup_thread()

    def _start_cleanup_thread(self):
        threading.Thread(target=self.__cleanup_containers, daemon=True).start()

    # noinspection PyMethodMayBeStatic
    def __cleanup_containers(self):
        while True:
            time.sleep(60)
            for function_name, container in list(cached_containers.items()):
                if function_name not in cached_containers:
                    logger.info(f"Stopping and removing container for "
                                f"{function_name} due to timeout.")
                    container.stop()
                    container.remove()
                    del cached_containers[function_name]
