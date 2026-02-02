import json
import requests
from bs4 import BeautifulSoup, Tag


def normalize_code_block(raw_text: str) -> str:
    """
    Normalize scraped code text by:
    1. Removing leading/trailing empty lines
    2. Collapsing multiple internal blank lines to one
    3. Preserving indentation and code structure
    """

    # Split into lines (preserves indentation)
    lines = raw_text.splitlines()

    # 1. Remove leading empty lines
    while lines and lines[0].strip() == "":
        lines.pop(0)

    # 2. Remove trailing empty lines
    while lines and lines[-1].strip() == "":
        lines.pop()

    # 3. Collapse multiple blank lines inside code
    normalized_lines = []
    previous_blank = False

    for line in lines:
        if line.strip() == "":
            if not previous_blank:
                normalized_lines.append("")
            previous_blank = True
        else:
            normalized_lines.append(line)
            previous_blank = False

    # Rejoin
    clean_code = "\n".join(normalized_lines)

    return f"CODE\n{clean_code}\n/CODE"




def scrape_page(url):

    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")
    main_div = soup.find("div", class_ = 'md-content')

    page_content = {
    "url" : None,
    "title" : None,
    "content" : []
    }
    
    page_content['url'] = url

    for children in main_div.descendants:


        # skipping note blocks 
        if children.find_parent("div",class_=["admonition", "note", "info", "tip"]):
            continue
        # skipping navigable block at the start of the page
        if children.find_parent('nav', class_ = "md-path"):
            continue

        # extracting title
        if children.name == "h1":
            page_content["title"] = children.get_text(strip = True)[:-1]
            page_content["content"].append({
                'type' : 'heading',
                'level' : 1,
                'text' : page_content['title']

            })
            continue
        #extracting subheadings
        if children.name in ['h2', 'h3', 'h4', 'h5', 'h6']:
            page_content['content'].append({
                'type' : 'heading',
                'level' : int(children.name[1]),
                'text' : children.get_text(strip = True)[:-1]

            })
            continue
        # extracting paragraphs
        if children.name == "p":
            text = children.get_text(" ", strip=True)
            if text:
                page_content["content"].append({
                    "type": "text",
                    "text": text
                })
            continue
        # extracting bullet points
        if children.name in ["ul", "ol"]:
            for li in children.find_all("li", recursive=False):
                text = li.get_text(" ", strip=True)
                if text:
                    page_content["content"].append({
                        "type": "list_item",
                        "text": text
                    })
            continue

        # extracting code blocks, keeping the structure as it is
        if isinstance(children, Tag) and "tabbed-content" in children.get("class", []):
            raw_code = children.get_text(strip=False)
            clean_code = normalize_code_block(raw_code)

            page_content["content"].append({
                "type": "code",
                "text": clean_code
            })
            # page_content["content"].append({
            #     'type' : 'code',
            #     'text' : children.get_text(strip=False)

            # })
            continue
        
        # # extracting code blocks, keeping the structure as it is, caputuuring highlights tag:
        if isinstance(children, Tag) and "highlight" in children.get("class", []) and not children.find_parent('div', class_ ="tabbed-content"):
            page_content["content"].append({
                'type' : 'code',
                'text' : children.get_text(strip=False)

            })
            continue
            

        continue
    return page_content

    



    