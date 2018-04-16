#!/usr/bin/env python3
import os
import re
import shutil
import requests
from bs4 import BeautifulSoup
from pyunpack import Archive


def download_file(url, dest):
    try:
        html_str = requests.get(url).text
        html = BeautifulSoup(html_str, 'html.parser')

        link_el = html.find('a', class_='download_bt')
        link_str_relative = link_el['href'].replace('file-download', 'start-download')
        link_str_absolute = 'http://baumanki.net' + link_str_relative

        _save_file(link_str_absolute, dest)
    except:
        print('Failed at file', url)
        raise


def _save_file(url, dest):
    os.makedirs(dest, exist_ok=True)

    with requests.get(url, stream=True) as r:
        filename = re.findall('filename="(.+?)"', r.headers['content-disposition'])[0]
        filepath = os.path.join(dest, filename)
        with open(filepath, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

    filepath_without_ext = '.'.join(filepath.split('.')[:-1])
    os.makedirs(filepath_without_ext, exist_ok=True)
    Archive(filepath).extractall(filepath_without_ext)

    os.remove(filepath)


if __name__ == '__main__':
    try:
        assert len(os.sys.argv) >= 3
        url = os.sys.argv[1]
        dest = os.sys.argv[2]
    except AssertionError:
        print('USAGE: python3 download_file.py URL DEST')
        exit(1)

    download_file(url, dest)
    
