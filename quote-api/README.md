# UF-API_GROUP (Quote API Branch)

This branch is for the development of the Quote API. When going to the quote page, a random quote from a csv file is returned, which includes the quote, the author, and the catagory from which the quote comes from.

Note: The API is working as is.

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
   ```

### Running

1. Run the program from the file location on your machine
   ```sh
   python quote.py
   ```
2. Navigate to the url in your browser
   ```sh
   http://localhost:8000/quote
   ```

### PATH Variable

If you are getting and import error when attemping to run the program saying that it can not find the modules to import, then the program may not be looking in the right locations for those packages. To check where the program is looking for the packages it needs, add these lines at the top of the program and run it:
```sh
import sys
print(sys.path)
```
If the file locations of where you have the packages installed is not listed when you attempt to run the prgram now, then you need to add those file locations to your system's PATH variable.

Learn more about PATH variables and how to edit them <a href="https://www.java.com/en/download/help/path.html">here.</a>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Acknowledgments

* [Webminer Quote Database](https://thewebminer.com/buy-famous-quotes-database)

<p align="right">(<a href="#readme-top">back to top</a>)</p>