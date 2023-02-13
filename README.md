# What Is This?

This is the repository for UF Open Source Club's API development group. We meet biweekly and program APIs for personal and public use.

# How to Get Started?

For most of our APIs we are using the Python API framework "Fast API." The basic imports are `fastapi` and `uvicorn[standard]`.

To get a simple, starter API going, simply run `pip install fastapi` and `pip install uvicorn[standard]` in your Python environment
to get those imports functional. `fastapi` is the main framework, whereas `uvicorn` is for testing the API on our localhost.

Include this bit of "Hello world" boilerplate in a `main.py` file...

```python

from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
	
```

And voila! If you run `uvicorn main:app --reload` in your terminal, it should get a test server up and running on
http://127.0.0.1:8000.
