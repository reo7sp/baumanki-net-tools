#!/usr/bin/env python3
import os
import requests
from bs4 import BeautifulSoup
from download_category import download_category
from tqdm import tqdm


def download_subject(url, dest):
    try:
        os.makedirs(dest, exist_ok=True)

        html_str = requests.get(url).text
        html = BeautifulSoup(html_str, 'html.parser')

        result_table = html.find(id='result_table')
        if result_table is None:
            return
        for link_el in tqdm(result_table.find_all('a'), desc=url):
            link_str_relative = link_el['href']
            if not 'filearray' in link_str_relative:
                continue
            link_str_absolute = 'http://baumanki.net' + link_str_relative
            name = link_el.string
            download_category(link_str_absolute, os.path.join(dest, name))
    except:
        print('Failed at subject', url)
        raise


if __name__ == '__main__':
    try:
        assert len(os.sys.argv) >= 3
        url = os.sys.argv[1]
        dest = os.sys.argv[2]
    except AssertionError:
        print('USAGE: python3 download_subject.py URL DEST')
        exit(1)

    download_subject(url, dest)
    
