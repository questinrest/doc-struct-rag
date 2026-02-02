import requests
from bs4 import BeautifulSoup
import re

def scrape_and_clean(url):
    
    response = requests.get(url)
    html_content = response.content

    soup = BeautifulSoup(html_content, "html.parser")

    for script in soup(["script", "style"]):
        script.extract()
    
    text = soup.get_text(separator=" ", strip = True)

    #cleaning excessive whitespaces
    clean_text = re.sub(r'\s+', ' ', text)

    return clean_text





