import requests
import uvicorn
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
from fastapi import FastAPI, APIRouter

# triya note - unique to this project is a problem of relative imports -
# if we run the file itself, from leetcode_constants import * works,
# but running it from main.py from the parent directory will not
# this is just accounting for that
if __name__ == "__main__":
    app = FastAPI()
    from leetcode_constants import *
else:
    app = APIRouter()
    from .leetcode_constants import *


@app.get("/lcapi/{username}")
def read_item(username: str):
    return leetcodeScrape(username)


class User:
    name: str  # LC Username
    completed_total: int  # Total completed questions
    completed_list: list[int]  # Index 0,1,2 correspond to easy, med, hard
    rank: int  # User's rank. Based off of number of completed problems.
    recent: bool  # If the user has completed a problem in the last 24 hours
    recent_problem: str = ""  # The user's most recent problem, if it exists

    def getAttributes(self):
        """
        Returns attributes in easily readable string format.
        """
        recent_line = (
            f"\t Their most recent problem was {self.recent_problem}.\n" if self.recent else ""
        )
        return (
            "Username: \t{self.name}\n"
            f"Rank: \t\t{self.rank}\n\n"
            f"This user is{' ' if self.recent else ' not '}active.\n"
            f"{recent_line}"
            f"\nNumber of completed problems: ({self.completed_total})\n"
            f"\tEasy: {self.completed_list[0]}\n"
            f"\tMedium: {self.completed_list[1]}\n"
            f"\tHard: {self.completed_list[2]}\n"
        )

    def __str__(self):
        """
        Override for printing the object, just for clarity's sake
        """
        return self.getAttributes()


def leetcodeScrape(username: str):
    # Initialize user object
    user = User()

    # Get the user's LC URL
    user.name = username

    # Initialize browser options for Selenium
    browser_options = ChromeOptions()

    # Enables headless mode for Selenium
    browser_options.add_argument("--headless=new")

    # Initialize Chrome web driver using browser options
    driver = Chrome(options=browser_options)

    # Opens URL using the web driver
    driver.get("https://leetcode.com/" + user.name)

    # Get Raw HTML
    try:
        r = requests.get("https://leetcode.com/" + user.name)
    except requests.exceptions.InvalidURL:
        return -1

    html_doc = bs(r.content, "html.parser")

    # Gets raw divs for user's number of completed problems by difficulty
    raw_completed = html_doc.find_all("span", class_=DIFF_DIV_CLASS)

    # Translates those divs into usable numbers
    user.completed_list = [int(r.get_text()) for r in raw_completed]
    user.completed_total = sum(user.completed_list)

    # Get raw rank
    raw_rank = html_doc.find("span", class_=RANK_DIV_CLASS).get_text()

    # Remove commas, assign rank
    user.rank = int(raw_rank.replace(",", ""))

    # Get the most recent problem, if any
    raw_recent = (
        WebDriverWait(driver, 10)
        .until(EC.element_to_be_clickable((By.XPATH, RECENT_DIV_CLASS)))
        .text
    )

    # If submitted recently (LC uses the format "23 hours ago" or "1 day ago")
    user.recent = "hour" in raw_recent
    if user.recent:
        user.recent_problem = driver.find_element(By.XPATH, RECENT_PROBLEM_DIV_CLASS).text

    # Shutdown web driver
    driver.quit()

    # Prints user data
    return user


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8080)
