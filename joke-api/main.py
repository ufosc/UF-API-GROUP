from fastapi import FastAPI
from profanity import profanity
from pathlib import Path
from fastapi import APIRouter
import json
import random
import openai

if __name__ == "__main__":
    app = FastAPI()
else:
    app = APIRouter()

jokes = []

API_NAME = "/jokes"

jokes = json.loads(open(f"{Path(__file__).parent.as_posix()}/final_jokes.json", "r").read())
config = json.loads(open(f"{Path(__file__).parent.as_posix()}/config.json", "r").read())

banned_words = config["banned_words"]
profanity_check = config["profanity_check"]
openai.api_key = config["open_ai_key"]

categorized_jokes = {
    "programming": [j for j in jokes if j["type"] == "programming"],
    "animal": [j for j in jokes if j["type"] == "animal"],
    "food": [j for j in jokes if j["type"] == "food"],
    "math": [j for j in jokes if j["type"] == "math"],
    "general": [j for j in jokes if j["type"] == "general"],
}

@app.get(API_NAME + "/")
def read_root():
    return {
        "Joke categories": ["general", "animal", "food", "math", "programming"],
        "Usage": ["/random", "/{category}", "/ai", "/ai/{category}"],
    }


@app.get(API_NAME + "/random")
def get_random_joke():
    return random.choice(jokes)

@app.get(API_NAME + "/ai")
def get_random_ai_joke():
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="tell me a joke",
        temperature=1,
        max_tokens=150,
        top_p=1,
        frequency_penalty=2,
        presence_penalty=1,
    )
    return response["choices"][0]["text"]

@app.get(API_NAME + "/ai/{category}")
def get_ai_joke(category: str):
    if category in config["banned_words"] or (
        profanity_check and profanity.contains_profanity(category)
    ):
        return {"Error": "That word is not allowed."}
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"tell me a {category} joke",
        temperature=1,
        max_tokens=150,
        top_p=1,
        frequency_penalty=2,
        presence_penalty=1,
    )
    return response["choices"][0]["text"]

@app.get(API_NAME + "/{category}")
def get_joke(category: str):
    try:
        j = random.choice(categorized_jokes[category])
        return j
    except:
        return {"Error": "Category does not exist."}


# uvicorn main:app --reload
