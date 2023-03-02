# UF-API-GROUP (LEETCODE API BRANCH)

This branch is for the development of the Leetcode API. Upon being given a username, `requests` and `BeautifulSoup` scrape and parse the necessary data *(number of completed problems, ranking, etc.)* This data is then stored in an object and is returned.

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
   pip install beautifulsoup4
   pip install requests
   pip install uvicorn
   ```

### How to use
Upon running the script, the API will be hosted on localhost:8080/lcapi

To query a user, simply add it to the end of the URL. example: localhost:8080/lcapi/cbloodsworth

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
