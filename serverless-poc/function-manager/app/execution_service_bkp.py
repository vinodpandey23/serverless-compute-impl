import json
import os

from docker.errors import ContainerError, APIError

from config import FUNCTIONS_DIR, cached_containers, cached_errors, \
    docker_client, logger


class ExecutionService:
    def __init__(self):
        logger.info("Initializing Execution Service")

    def execute_function(self, function_name, payload):
        function_dir = os.path.join(FUNCTIONS_DIR, function_name)
        handler_path = os.path.join(function_dir, "handler.py")

        if not os.path.exists(handler_path):
            error_msg = f"Handler file '{handler_path}' not found."
            logger.error(error_msg)
            return {"success": False, "error": error_msg}

        if function_name in cached_errors:
            raise cached_errors[function_name]

        container = cached_containers.get(function_name)

        if container and container.status == 'running':
            logger.info(f"Reusing warm container for {function_name}")
        else:
            logger.info(
                f"Cold start: Initializing container for {function_name}")
            container = self._start_container(function_name)
            cached_containers[function_name] = container

        response = self._invoke_function(container, function_name, payload)
        return response

    # noinspection PyMethodMayBeStatic
    def _start_container(self, function_name):
        function_dir = os.path.abspath(
            os.path.join(FUNCTIONS_DIR, function_name))
        if not os.path.exists(function_dir):
            error = FileNotFoundError(f"Function '{function_name}' not found.")
            cached_errors[function_name] = error
            raise error

        logger.info(f"Starting container for {function_name}...")
        try:
            container = docker_client.containers.run(
                "serverless-python-function-base:latest",
                command=["sleep", "infinity"],
                volumes={FUNCTIONS_DIR: {'bind': FUNCTIONS_DIR, 'mode': 'rw'}},
                working_dir="/app",
                detach=True
            )
            container.reload()

            if container.status != 'running':
                logs = container.logs().decode('utf-8')
                logger.error(f"Container for {function_name} crashed on "
                             f"startup:\n{logs}")
                container.remove()
                raise RuntimeError(f"Container for {function_name} crashed "
                                   f"on startup. Logs:\n{logs}")

            logger.info(f"Container for {function_name} started successfully.")
            return container

        except ContainerError as e:
            logger.error(f"Container error for {function_name}: {e}")
            raise
        except APIError as e:
            logger.error(f"Docker API error for {function_name}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error while starting container for "
                         f"{function_name}: {e}")
            raise

    # noinspection PyMethodMayBeStatic
    def _invoke_function(self, container, function_name, payload):
        try:
            logger.info(f"Invoking function in container {container.id}...")
            exec_result = container.exec_run(
                cmd=["python", "-u", "runner.py", function_name,
                     json.dumps(payload)], workdir="/app")

            if exec_result.exit_code == 0:
                response = exec_result.output.decode(
                    'utf-8') if exec_result.output else ""
                logger.info("Function execution completed.")
                return response
            else:
                logger.info(f"Exec Result: {exec_result}")
                logger.info(f"Exec Output: {exec_result.output}")
                logger.error(f"Function execution failed with exit "
                             f"code: {exec_result.exit_code}")
        except Exception as e:
            logger.error(f"Failed to invoke function: {e}")
            raise
