import json

import requests
from bs4 import BeautifulSoup

URL = 'https://www.google.com/'


def get_html(url):
    search = input('Something to search:\t')
    r = requests.get(url, params={'q': search})
    print(r.url)
    return r.content


def parse(html):
    soup = BeautifulSoup(html, "lxml")
    return soup.prettify()


def main():

    html = get_html(URL)
    print(html)
    

if __name__ == '__main__':
    main()
