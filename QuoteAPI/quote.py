from fastapi import FastAPI
from random import randint

app = FastAPI()

@app.get("/quote")
async def get_quote():
    file = open("quotes_all.csv", 'r')
    random_num = randint(2, 7967)
    data = ""
    while random_num > 0:
        data = file.readline()
        random_num -= 1

    answer = data.split(';')
    fixed_category = answer[2][0:len(answer[2]) - 1]
    answer[2] = fixed_category
    return {"quote": answer[0], "author": answer[1], "category": answer[2]}
