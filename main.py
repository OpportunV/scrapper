import json
from random import choice, shuffle
from typing import List

import requests
from bs4 import BeautifulSoup

URL = 'https://www.google.com/search'
HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0'}
FILENAME = "tmp"


def get_html(url):
    global FILENAME
    search = input('Something to search:\t')
    FILENAME = search
    r = requests.get(url, params={'q': search}, headers=HEADERS)
    return r.content


def pick_links(html, n=3):
    soup = BeautifulSoup(html, 'lxml')
    links = [i['href'] for i in soup.find_all('a', href=True)
             if i['href'].startswith('http') and 'google' not in i['href']]
    shuffle(links)
    return [links.pop() for _ in range(n)]


def parse_links(links: List):
    data = []
    for link in links:
        obj = {'link': link}
        soup = BeautifulSoup(requests.get(link, allow_redirects=True, headers=HEADERS).content, 'lxml')
        
        try:
            obj['h1'] = soup.find('h1').text
        except AttributeError:
            obj['h1'] = 'wooops'
            
        img = choice(soup.find_all('img', src=True))
        img_src = img['src']
        if not img_src.startswith('http'):
            img_src = f'{".".join(link.split(".")[:-1])}.{link.split(".")[-1].split("/")[0]}/{img_src.lstrip("/")}'
        
        try:
            img_alt = img['alt']
            if img_alt:
                obj['img_info'] = img_alt
        except KeyError:
            pass
        
        obj['img_src'] = img_src
        
        parent = img.parent
        try:
            desc = '/n'.join([p.text for p in parent.find_all('p')])
        except AttributeError:
            desc = ''
        
        if not desc:
            try:
                desc = '/n'.join([d.text for d in parent.find_all('div')])
            except AttributeError:
                pass
        if not desc:
            try:
                desc = parent.find('p').text
            except AttributeError:
                pass
            
        parent = parent.parent
        if not desc:
            try:
                desc = '/n'.join([p.text for p in parent.find_all('p')])
            except AttributeError:
                pass
        if not desc:
            try:
                desc = '/n'.join([d.text for d in parent.find_all('div')])
            except AttributeError:
                pass
        if not desc:
            try:
                desc = parent.find('p').text
            except AttributeError:
                pass

        obj['desc'] = desc if desc else 'Wooops! nothing i can do'
        data.append(obj)
    return data


def write_data(data):
    with open(f'{FILENAME}.json', 'w', encoding='utf8') as f_out:
        json.dump(data, f_out, indent=2, ensure_ascii=False)


def main():
    html = get_html(URL)
    links = pick_links(html)
    data = parse_links(links)
    write_data(data)
    

if __name__ == '__main__':
    main()
