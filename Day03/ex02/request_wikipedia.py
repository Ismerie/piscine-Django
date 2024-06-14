import sys
import json
import requests
import dewiki

def request_wiki(page):
    URL = "https://fr.wikipedia.org/w/api.php"

    PARAMS = {
        "action": "parse",
        "page": page,
        "prop": "wikitext",
        "format": "json",
        "redirects": "true"
    }
    try:
        r = requests.get(url=URL, params=PARAMS)
        r.raise_for_status()
        data = json.loads(r.text)
        if data.get("error") is not None:
            print(data["error"]["info"])
            sys.exit(1)
        data_wiki = dewiki.from_string(data["parse"]["wikitext"]["*"])
    except Exception as e:
        print(e)
        sys.exit(1)
    return data_wiki

def main():
    if len(sys.argv) != 2:
        return print("Usage: python3 request_wikipedia.py <page")
    try:
        words = sys.argv[1].strip().split()
        page = " ".join(words)
        data = request_wiki(page)
        page = page.replace(' ', '_')
        file = open("{}.wiki".format(page), "w")
        file.write(data)
        file.close
    except Exception as e:
        return print(e)

if __name__ == '__main__':
    main()