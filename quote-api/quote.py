import uvicorn
from pathlib import Path
from fastapi import FastAPI, APIRouter
from random import randint

if __name__ == "__main__":
    app = FastAPI()
else:
    app = APIRouter()


@app.get("/quote")
async def get_quote():
    # triya - workaround to quotes_all.csv being in possibly different places
    # __file__ is always in the same place regardless if this is being run on
    # its own or not, so just take advantage of that
    file = open(f"{Path(__file__).parent.as_posix()}/quotes_all.csv", "r")
    random_num = randint(2, 7967)
    data = ""
    while random_num > 0:
        data = file.readline()
        random_num -= 1

    answer = data.split(";")
    fixed_category = answer[2][0 : len(answer[2]) - 1]
    answer[2] = fixed_category
    return {"quote": answer[0], "author": answer[1], "category": answer[2]}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
