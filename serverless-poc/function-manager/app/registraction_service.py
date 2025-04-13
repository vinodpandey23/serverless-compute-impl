import os
import shutil
import zipfile

from config import FUNCTIONS_DIR, logger


class RegistrationService:
    # noinspection PyMethodMayBeStatic
    def register_function(self, function_name, zip_file):
        function_dir = os.path.join(FUNCTIONS_DIR, function_name)

        if os.path.exists(function_dir):
            logger.info(f"Removing existing directory for {function_name}...")
            shutil.rmtree(function_dir)

        os.makedirs(function_dir, exist_ok=True)
        logger.info(
            f"Created new directory for {function_name} at {function_dir}")

        zip_file.file.seek(0)
        try:
            with zipfile.ZipFile(zip_file.file, 'r') as zip_ref:
                zip_ref.extractall(function_dir)
            logger.info(f"Extracted zip contents for {function_name} into "
                        f"{function_dir}")
        except zipfile.BadZipFile:
            error_msg = f"Invalid zip file provided for {function_name}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}

        handler_path = os.path.join(function_dir, "handler.py")
        if not os.path.exists(handler_path):
            shutil.rmtree(function_dir)
            error_msg = f"handler.py not found in {function_dir}."
            logger.error(error_msg)
            return {"success": False, "error": error_msg}

        return {
            "success": True,
            "message": f"Function {function_name} registered successfully."
        }
