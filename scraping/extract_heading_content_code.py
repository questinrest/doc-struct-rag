import json
import requests
from bs4 import BeautifulSoup


url = "https://fastapi.tiangolo.com/python-types/"

response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

#print(soup.find('h1')) # extracting Heading


all_specific_divs = soup.find_all("div", class_="tabbed-set tabbed-alternate")

if all_specific_divs:
    print("\nFound div content using find_all():")
    for div in all_specific_divs:
        print(div.get_text(strip=True))
        break
else:
    print("No divs found.")