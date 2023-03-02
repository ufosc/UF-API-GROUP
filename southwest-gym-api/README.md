# UF-API-GROUP (SOUTHWEST GYM API BRANCH)

This branch is for the development of the Southwest Gym API. This is functional as-is.

This scrapes the Southwest Gym website in order to get each location and their current status, how many people they have, and how full they are. Results are cached for 5 minutes for speed.

This is also an example of how to use `aiohttp`, which can be thought of as the asynchronous equivalent to `requests`.
As FastAPI is asynchronous itself, using `aiohttp` is a natural fit.

Currently made by [PythiaUF](https://github.com/PythiaUF).

<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up UF-API-GROUP locally.
To get a local copy up and running follow these simple example steps.

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/ufosc/UF-API-GROUP.git
   ```
2. Install python packages
   ```sh
   pip install fastapi[all]
   pip install fastapi-cache2
   pip install aiohttp
   pip install beautifulsoup4
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [FastAPI](https://fastapi.tiangolo.com/)
* [aiohttp](https://docs.aiohttp.org/en/stable/)
* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>