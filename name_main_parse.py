#!/usr/bin/env python3
import re
import ast
import logging
import argparse

FASTAPI_INIT = re.compile(r"(?P<app_name>\w+) ?= ?FastAPI\((?P<api_params>.*)\)")


def replace_old_init(a_match: re.Match) -> str:
    app_name = a_match["app_name"]
    api_params = a_match["api_params"]
    return (
        f'if __name__ == "__main__":\n    {app_name} = FastAPI({api_params})\nelse:\n  '
        f"  {app_name} = APIRouter()"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--silent", action="store_true")
    parser.add_argument("files", nargs="+", type=argparse.FileType("r+"))

    args = parser.parse_args()

    logger = logging.getLogger("name_main")

    if args.silent:
        logger.setLevel(logging.CRITICAL)
    else:
        logger.setLevel(logging.INFO)
        logging.basicConfig()

    for f in args.files:
        logger.info(f"Processing {f.name}...")

        text: str = f.read()

        node = ast.parse(text)

        found_fastapi_main = False
        found_uvicorn_run = False

        for elem in node.body:
            if not (
                isinstance(elem, ast.If)
                and isinstance(elem.test, ast.Compare)
                and isinstance(elem.test.left, ast.Name)
                and elem.test.left.id == "__name__"
                and isinstance(elem.test.ops[0], ast.Eq)
                and isinstance(elem.test.comparators[0], ast.Str)
                and elem.test.comparators[0].value == "__main__"
            ):
                continue

            if not found_fastapi_main:
                found_fastapi = any(
                    isinstance(subelem, ast.Assign)
                    and isinstance(subelem.value, ast.Call)
                    and isinstance(subelem.value.func, ast.Name)
                    and subelem.value.func.id == "FastAPI"
                    for subelem in elem.body
                )

                found_apirouter = any(
                    isinstance(subelem, ast.Assign)
                    and isinstance(subelem.value, ast.Call)
                    and isinstance(subelem.value.func, ast.Name)
                    and subelem.value.func.id == "APIRouter"
                    for subelem in elem.orelse
                )

                if found_fastapi and found_apirouter:
                    found_fastapi_main = True

            elif not found_uvicorn_run:
                found_uvicorn_run = any(
                    isinstance(subelem, ast.Expr)
                    and isinstance(subelem.value, ast.Call)
                    and isinstance(subelem.value.func, ast.Attribute)
                    and isinstance(subelem.value.func.value, ast.Name)
                    and subelem.value.func.value.id == "uvicorn"
                    and subelem.value.func.attr == "run"
                    for subelem in elem.body
                )

            else:
                continue

        if not found_fastapi_main:
            if a_match := FASTAPI_INIT.search(text):
                text = FASTAPI_INIT.sub(replace_old_init, text)
            else:
                logger.info("Not a FastAPI app, moving on.")
                continue

        if not found_uvicorn_run:
            text = text.strip()
            if "import uvicorn" not in text:
                text = "import uvicorn\n" + text
            text += (
                '\n\nif __name__ == "__main__":\n    uvicorn.run(app, host="localhost", port=8000)'
            )

        text = text.strip()
        f.seek(0)
        f.write(text)

        if not found_fastapi_main:
            logger.info("Found old FastAPI init, replaced with FastAPI/APIRouter hybrid.")
        if not found_uvicorn_run:
            logger.info("Added uvicorn.run() to bottom of file.")

        if found_fastapi_main and found_uvicorn_run:
            logger.info(
                "File already has FastAPI/APIRouter hybrid and uvicorn.run(), nothing to do."
            )
