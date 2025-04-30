from bs4 import BeautifulSoup

def parse_all_data(html_page):
    global soup
    soup = BeautifulSoup(html_page, "lxml")

def clean_text():
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    clean_text = soup.get_text(separator="\n", strip=True)
    return clean_text

def all_href_links():
    all_links = []
    for a_tag in soup.find_all('a', href=True):
        all_links.append(a_tag['href'])

    return all_links