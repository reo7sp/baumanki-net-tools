#!/usr/bin/env python3
import os
import requests
from bs4 import BeautifulSoup

from constants import ROOT_URL
from download_file import download_file
from tqdm import tqdm


def _check_is_valid_file_url(link):
    parts = link.split('-')
    if len(parts) == 0:
        return False
    return parts[0].isdigit()


def download_category(url, dest):
    try:
        os.makedirs(dest, exist_ok=True)

        html_str = requests.get(url).text
        html = BeautifulSoup(html_str, 'html.parser')

        result_table = html.find(id='subject-table')
        if result_table is None:
            return
        for link_el in tqdm(result_table.find_all('a'), desc=url):
            link_str_relative = link_el['href']
            if not _check_is_valid_file_url(link_str_relative):
                continue
            link_str_absolute = url + '/' + link_str_relative
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

