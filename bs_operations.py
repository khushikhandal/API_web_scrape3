from bs4 import BeautifulSoup
import re


def parse_all_data(html_page):
    #putting html_page data in soup var so that bs4 can parse it
    global soup
    soup = BeautifulSoup(html_page, "lxml")

def clean_text():
    # Remove script and style elements
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    clean_text = soup.get_text(separator="\n", strip=True)
    return clean_text

def all_href_links():
    all_links = []
    for a_tag in soup.find_all('a', href=True):
        all_links.append(a_tag['href'])

    return all_links #list of all links

def social_media_links():
    social_links = []
    for link in all_href_links():
        if any(social in link for social in ["facebook.com", "instagram.com", "linkedin.com", "twitter.com", "x.com", "youtube.com"]):
            social_links.append(link)

    return social_links #list of all social media links

def get_emails():
    emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", soup.get_text())
    return emails #list of all emails

def get_phone_nos():
    phones = re.findall(r"\+?\d[\d\s\-\(\)]{7,}\d", soup.get_text())
    return phones #list of all numbers