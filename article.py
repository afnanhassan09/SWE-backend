from bs4 import BeautifulSoup
import requests
import re
from readability import Document


def clean_text(text):
    text = re.sub(r"<.*?>", "", text)
    text = re.sub(r"\{\{.*?\}\}", "", text)

    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\n+", "\n", text)

    text = text.strip()

    return text


def extract_main_content(url):
    response = requests.get(url)
    doc = Document(response.text)
    soup = BeautifulSoup(doc.summary(), "html.parser")
    return clean_text(soup.text)
