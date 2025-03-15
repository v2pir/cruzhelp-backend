import requests
from bs4 import BeautifulSoup
import os

def run(web):
    # create data directory
    directory = "data"
    try:
        os.mkdir("data")
    except FileExistsError:
        print(f"Directory '{directory}' already exists.")

    # get the website
    page = requests.get(web)

    # get all the text from the website
    soup = BeautifulSoup(page.content, "lxml")
    text = soup.text

    # get all subpages in the website
    links = soup.find_all('a')

    pages = []
    for link in links:
        href = link.get('href')
        if href:
            if href[:5] == "https":
                continue
            pages.append(web+str(href))

    pages = list(set(pages))

    text = ""

    for i in pages:
        page = requests.get(i)

        # get all the text from the website
        soup = BeautifulSoup(page.content, "lxml")
        text +=  soup.text

    # open the .md file and write all the text there
    with open("data/data.md", 'w') as f:
        for t in text:
            f.write(t)

    # close the file
    f.close()