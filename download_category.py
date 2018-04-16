#!/usr/bin/env python3
import os
import requests
from bs4 import BeautifulSoup
from download_file import download_file
from tqdm import tqdm


def download_category(url, dest):
    try:
        html_str = requests.get(url).text
        html = BeautifulSoup(html_str, 'html.parser')

        for link_el in tqdm(html.find(id='table_with_file_to_download').find_all('a')):
            link_str_relative = link_el['href']
            if not 'filearray' in link_str_relative:
                continue
            link_str_absolute = 'http://baumanki.net' + link_str_relative
            name = link_el.string
            download_file(link_str_absolute, os.path.join(dest, name))
    except:
        print('Failed at category', url)
        raise


if __name__ == '__main__':
    try:
        assert len(os.sys.argv) >= 3
        url = os.sys.argv[1]
        dest = os.sys.argv[2]
    except AssertionError:
        print('USAGE: python3 download_category.py URL DEST')
        exit(1)

    download_category(url, dest)
    
