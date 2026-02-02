import requests
from bs4 import BeautifulSoup


# step 1 : fetch the web page

url =  "https://fastapi.tiangolo.com/async"

response = requests.get(url)

html_content = response.content

# step 2 : parse the content

soup = BeautifulSoup(html_content, "html.parser")

#print(soup)


for script in soup("script", "style"): # filter out scripts and style tags
    script.extract()


#text = soup.get_text() # remove all the tags, but when you will use directly, order will remain same, space and if something came up in different lines it will stay same.
# we will use separater, to closen the gaps, not all but most of it, and coupled with strip = True, almost all of the spaces would go awa

text = soup.get_text(separator=" ", strip = True) # exact text content
 

print(text)
 

