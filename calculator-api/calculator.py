from fastapi import FastAPI
from pydantic import BaseModel
from math import log

app = FastAPI()


class Operands(BaseModel):  # This is the format of the JSON Request for these functions
    x: int
    y: int


@app.post("/add")
async def api_add(operands: Operands):  # Finds the sum of x and y
    return operands.x + operands.y


@app.post("/sub")
async def api_sub(operands: Operands):  # Finds the difference between x and y
    return operands.x - operands.y


@app.post("/mul")
async def api_mul(operands: Operands):  # Finds the product of x and y
    return operands.x * operands.y


@app.post("/div")
async def api_div(operands: Operands):  # Finds the quotient of x and y
    return operands.x / operands.y


@app.post("/mod")
async def api_mod(operands: Operands):  # Finds the remainder of x and y
    return operands.x % operands.y


@app.post("/pow")
async def api_pow(operands: Operands):  # Finds the power of x and y
    return operands.x**operands.y


@app.post("/root")
async def api_root(operands: Operands):  # Finds the root of x and y
    return operands.x**(1/operands.y)


@app.post("/log")
async def api_log(operands: Operands):  # Finds the log of x base y
    return log(operands.x, operands.y)
