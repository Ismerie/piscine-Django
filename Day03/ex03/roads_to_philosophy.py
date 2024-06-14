import sys
import requests
from bs4 import BeautifulSoup


def roads_to_philosophy(name_page, titles):
    URL = 'https://en.wikipedia.org/wiki/{page}'.format(page=name_page)
    try:
        res = requests.get(url=URL)
        res.raise_for_status()
    except Exception as e:
        raise e
    soup = BeautifulSoup(res.text, 'html.parser')
    title = soup.find(id='firstHeading').text
    if title in titles:
        print("it leads to an infinite loop !")
        return None
    elif title == "Philosophy":
        return title
    titles.append(title)
    content = soup.find(id='mw-content-text')
    allLinks = content.select('p > a')
    for link in allLinks:
        if link.get('href') is not None and link['href'].startswith('/wiki/')\
        and not link['href'].startswith('/wiki/Wikipedia:') and not link['href'].startswith('/wiki/Help:'):
            page_found = link['href'].replace("/wiki/", "")
            return page_found
    print("It leads to a dead end !")
    return None

def main():
    if len(sys.argv) != 2:
        return print("Usage: python3 roads_to_philosophy <string>")
    page = sys.argv[1]
    titles = []
    try:
        while True:
            page = roads_to_philosophy(page, titles)
            if page is None:
                return
            if page == "Philosophy":
                titles.append(page)
                for element in titles:
                    print(element)
                print(f'{len(titles)} roads from {titles[0]} to {titles[len(titles) - 1]}')
                break
    except Exception as e:
        print(f"Error: {e}")
        return
    
if __name__ == '__main__':
    main()