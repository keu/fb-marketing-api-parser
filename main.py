import requests
from bs4 import BeautifulSoup


class FacebookAPIParser:
    BASE_URL = 'https://developers.facebook.com/docs/marketing-api/reference/{}#fields'

    def __init__(self):
        self.parsed_endpoints = {}

    def scan_entities(self, entities):
        for entity in entities:
            self.scan_entity_api(self.BASE_URL.format(entity))

        for url, attrs in self.parsed_endpoints.items():
            print(url)
            for attr_name, attr_type in attrs:
                print(f"{attr_name}: {attr_type}")

    def scan_entity_api(self, url):
        print("scanning", url)
        if url in self.parsed_endpoints:
            print("found in parsed, skipping...")
            return
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'html.parser')
        p = soup.find("h3", text="Fields")
        table = p.parent.find("table")
        attrs = []
        for row in table.find_all("tr"):
            cells = row.find_all("td")
            if not cells:
                continue
            divs = cells[0].find_all("div")
            attr_name = divs[0].find("code").get_text()
            href = divs[1].find("a", href=True)
            if href:
                print('Found link, navigating', href)
                self.scan_entity_api(href['href'])
            attr_type = divs[1].get_text()
            attrs.append((attr_name, attr_type))

        self.parsed_endpoints[url] = attrs


def main():
    entities = [
        'ad-creative',
        'ad-campaign-group',
        'ad-campaign',
        'adgroup',
        'ads-insights'
    ]

    parser = FacebookAPIParser()
    parser.scan_entities(entities)


main()
