import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path


def load_handler(function_name):
    function_dir = Path(f"/mnt/functions/{function_name}")
    if not function_dir.exists():
        raise FileNotFoundError(
            f"No directory found for function: {function_name}")

    # Add function directory to sys.path
    sys.path.insert(0, str(function_dir))

    handler_path = function_dir / "handler.py"
    if not handler_path.exists():
        raise FileNotFoundError(
            f"No handler.py found for function: {function_name}")

    # Install dependencies if present
    install_dependencies(function_name)

    # Load handler module dynamically
    spec = importlib.util.spec_from_file_location("handler", str(handler_path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.handler


def install_dependencies(function_name):
    requirements_path = os.path.join("/mnt/functions", function_name,
                                     "requirements.txt")
    # Check if deps are already installed (e.g., venv/lib has packages)
    marker_file = os.path.join("/mnt/functions", function_name,
                               ".deps_installed")
    if os.path.exists(requirements_path) and not os.path.exists(marker_file):
        subprocess.run(
            ["/app/venv/bin/pip", "install", "-r", requirements_path],
            check=True, capture_output=True, text=True
        )
        # Mark as installed to avoid re-running
        with open(marker_file, "w") as f:
            f.write("done")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: runner.py <function_name> <payload>", file=sys.stderr)
        sys.exit(1)

    funct_name = sys.argv[1]
    payload = sys.argv[2]

    handler = load_handler(funct_name)
    result = handler(json.loads(payload))
    print(json.dumps(result))

