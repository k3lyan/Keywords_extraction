from bs4 import BeautifulSoup
import requests
import re
import logging

logger = logging.getLogger('root')

def line_cleaner(paragraph):
    return re.sub(r"[\n\r]", r"", paragraph)

def webscrap(url):
    page_response = requests.get(url, timeout=5)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    paragraphs = page_content.find_all("p")   
    paragraphs.extend(page_content.find_all("title"))
    return [line_cleaner(p.text).strip('  ') for p in paragraphs]


if __name__ == '__main__':
    url = 'https://blog.teckiki.io/keywords-extraction-using-k-truss/'
    print(webscrap(url))
