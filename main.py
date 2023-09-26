import importlib
import importlib.util
from warnings import warn
from pathlib import Path

import uvicorn
from fastapi import APIRouter, FastAPI


# python 3.8 doesn't have this natively :(
def remove_prefix(text: str, prefix: str):
    return text[len(prefix) :] if text.startswith(prefix) else text


app = FastAPI()

parent_name = str(Path(__file__).parent.as_posix())
paths_of_python_files = Path(__file__).parent.glob("*/*.py")

for a_path in paths_of_python_files:
    actual_path = str(a_path.as_posix())

    # so we have the actual full path of the file now, which is great
    # but what we want to do is make this a relative path compared to main
    # what we do is remove the path up to the directory this file is in
    # (and remove the / after that too), remove the .py at the end, and make
    # slashes to periods
    # for example: UF-API-GROUP/directory/file.py becomes directory.file
    as_module = remove_prefix(actual_path, parent_name)
    if as_module[0] == "/":
        as_module = as_module[1:]
    as_module = as_module[:-3]
    as_module = as_module.replace("/", ".")

    # just in case
    module_name = importlib.util.resolve_name(as_module, None)

    try:
        module = importlib.import_module(module_name)
    except ImportError as e:
        warn(f"Could not import module {module_name}: {e}")
        continue

    possible_router = getattr(module, "app", None)
    if not isinstance(possible_router, APIRouter):
        continue

    app.include_router(possible_router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8080)
