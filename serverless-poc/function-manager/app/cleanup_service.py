import threading
import time

from docker.errors import APIError

from config import cached_containers, logger, WARM_UP_TIME


class CleanupService:
    def __init__(self):
        logger.info("Initializing Cleanup Service")
        self.__lock = threading.Lock()
        self.__container_timestamps = {}
        self.__start_cleanup_thread()

    def __start_cleanup_thread(self):
        thread = threading.Thread(target=self._cleanup_containers, daemon=True)
        thread.start()

    def _cleanup_containers(self):
        while True:
            try:
                current_time = time.time()
                with self.__lock:
                    expired_keys = []
                    for function_name, container in list(
                            cached_containers.items()):
                        if container.status != "running":
                            expired_keys.append(function_name)
                        elif function_name in self.__container_timestamps:
                            creation_time = self.__container_timestamps[
                                function_name]
                            if current_time - creation_time > WARM_UP_TIME:
                                expired_keys.append(function_name)

                    for function_name in expired_keys:
                        container = cached_containers.get(function_name)
                        if container:
                            self._cleanup_container(function_name, container)
                            del cached_containers[function_name]

                    for function_name in list(
                            self.__container_timestamps.keys()):
                        if function_name not in cached_containers:
                            self.__container_timestamps.pop(function_name)

                time.sleep(60)
            except Exception as e:
                logger.error(f"Error in cleanup thread: {e}")
                time.sleep(10)

    def _cleanup_container(self, function_name, container):
        try:
            if container.status == "running":
                container.stop(timeout=10)
            container.remove()
            logger.info(
                f"Cleaned up container {container.id} for {function_name}")
            with self.__lock:
                self.__container_timestamps.pop(function_name, None)
        except APIError as e:
            logger.error(f"Failed to clean up container {container.id} "
                         f"for {function_name}: {e}")
        except Exception as e:
            logger.error(
                f"Unexpected error cleaning up container {container.id}: {e}")

    def register_container(self, function_name, container):
        with self.__lock:
            self.__container_timestamps[function_name] = time.time()
