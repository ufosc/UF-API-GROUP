import typing
from html import unescape
from datetime import datetime

import aiohttp
from bs4 import BeautifulSoup
from fastapi import FastAPI, APIRouter
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache
from pydantic import BaseModel
import uvicorn


SOUTHWEST_GYM_URL = (
    "https://connect2concepts.com/connect2/?type=circle&key=8E2C21D2-6F5D-45C1-AF9E-C23AEBFDA68B"
)


# python 3.8 doesn't have this natively :(
def remove_prefix(text: str, prefix: str):
    return text[len(prefix) :] if text.startswith(prefix) else text


# in python, PlaceData represents something like:
# {
#     "name": "NAME",
#     "closed": CLOSED,
#     "count": COUNT,
#     "percent": PERCENT,
#     "last_updated": DATE_IN_ISOFORMAT,
# }
class PlaceData(BaseModel):
    name: str
    closed: bool
    count: int
    percent: float
    last_updated: datetime


if __name__ == "__main__":
    app = FastAPI()
else:
    app = APIRouter(prefix="/gymstats")


@app.get("/")
@cache(expire=60 * 5)
async def gymstats() -> typing.List[PlaceData]:
    place_data: typing.List[PlaceData] = []

    # note: we need to fake a valid user agent to get past their very basic security system,
    # so i'm just using my own from my own browser lol
    async with aiohttp.ClientSession() as session:
        async with session.get(
            SOUTHWEST_GYM_URL,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101"
                    " Firefox/109.0"
                )
            },
        ) as resp:
            soup = BeautifulSoup(await resp.text(), "html.parser")

    # each room has a circle graph and some text underneath it - this line gets
    # every room by finding the "group" that holds those two things
    each_place_graph = soup.find_all("div", class_="col-md-3 col-sm-6")

    for place_graph in each_place_graph:
        # this will get us the circle graph that is rendered on screen via a library - no idea how,
        # but the important part is is that this contains some very useful parameters for us
        circle_chart = place_graph.find("div", class_="circleChart")
        # <div class="circleChart" data-fcolor="#FFF200" data-isclosed="1" data-lastcount="0" data-percent="0"></div>

        # we can get data through circle_chart["data-X"]
        # worth noting is that the last count is actually the true percent, while the percent is the rendered percent on the website... it's weird
        place_percent = float(circle_chart["data-lastcount"])
        place_is_closed = circle_chart["data-isclosed"] == "1"

        # the text-align "group" in this is what holds the text, which is what we want for the other info
        place_text = str(place_graph.find("div", style="text-align:center;"))
        # place text looks like this:
        # <div style="text-align:center;">ROOM NAME<br/><span style="color:COLOR">(STATUS)</span><br/>Last Count: COUNT<br/>Updated: TIME a la 02/03/2023 11:23 AM</div>

        # the place name is in between the initial div style stuff and the first br, so this gets that text there
        place_name = (
            remove_prefix(place_text, '<div style="text-align:center;">')
            .split("<br/>", maxsplit=1)[0]
            .strip()
        )
        # unescape the names so it looks nicer
        place_name = unescape(place_name)

        # the count for the place is after the "Last Count: " string always and before the next br
        place_count = int(
            place_text.split("Last Count: ", maxsplit=1)[1].split("<br/>", maxsplit=1)[0].strip()
        )

        # the last updated string is in a weird format
        # first we want to get it, then convert it to a more standard datetime
        # orjson will handle converting it to an iso string
        place_last_updated_str = (
            place_text.split("Updated: ", maxsplit=1)[1].split("</div>", maxsplit=1)[0].strip()
        )
        place_last_updated = datetime.strptime(place_last_updated_str, "%m/%d/%Y %I:%M %p")

        place_data.append(
            PlaceData(
                name=place_name,
                closed=place_is_closed,
                count=place_count,
                percent=place_percent,
                last_updated=place_last_updated,
            )
        )

    return place_data


@app.on_event("startup")
async def startup():
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8080)
