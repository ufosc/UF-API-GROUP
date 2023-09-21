import uvicorn
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from math import log

if __name__ == "__main__":
    app = FastAPI()
else:
    app = APIRouter()


class Operands(BaseModel):  # This is the format of the JSON Request for these functions
    x: int
    y: int


@app.post("/calc/add")
async def api_add(operands: Operands):  # Finds the sum of x and y
    return operands.x + operands.y


@app.post("/calc/sub")
async def api_sub(operands: Operands):  # Finds the difference between x and y
    return operands.x - operands.y


@app.post("/calc/mul")
async def api_mul(operands: Operands):  # Finds the product of x and y
    return operands.x * operands.y


@app.post("/calc/div")
async def api_div(operands: Operands):  # Finds the quotient of x and y
    return operands.x / operands.y


@app.post("/calc/mod")
async def api_mod(operands: Operands):  # Finds the remainder of x and y
    return operands.x % operands.y


@app.post("/calc/pow")
async def api_pow(operands: Operands):  # Finds the power of x and y
    return operands.x**operands.y


@app.post("/calc/root")
async def api_root(operands: Operands):  # Finds the root of x and y
    return operands.x ** (1 / operands.y)


@app.post("/calc/log")
async def api_log(operands: Operands):  # Finds the log of x base y
    return log(operands.x, operands.y)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
