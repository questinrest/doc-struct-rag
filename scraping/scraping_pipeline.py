from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin
from .scrape_page import scrape_page


## loading the URL JSON

# with open("url.json", 'r') as urls:
#     url_list = json.load(urls)


## prepare base URL
#base_url = 'https://fastapi.tiangolo.com/'


## function to scrape all the urls and dumping them into a json for future use

def scrape_all_pages(base_url, url_list):
    pages = []
    for url in url_list:
        final_url = urljoin(base_url, url)
        pages.append(scrape_page(final_url))
    
    ## dumping the content into JSON
    with open("document.json", "w") as doc:
        json.dump(pages, doc, indent = 4)


    