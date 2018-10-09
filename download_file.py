#!/usr/bin/env python3
import os
import re
import shutil
import traceback
import time
import requests
from bs4 import BeautifulSoup
from pyunpack import Archive

from constants import ROOT_URL


def download_file(url, dest):
    for i in range(3):
        try:
            _download_file(url, dest)
            return
        except:
            print('Failing at file {}. Retry {}/3...'.format(url, i+1))
            if i == 0:
                traceback.print_exc()
            time.sleep(10)
    print('Failed at file {}. Skip. Reported to log.txt'.format(url))
    _report_fail(url)


def _download_file(url, dest):
    try:
        os.makedirs(dest)
    except:
        return  # already downloaded

    html_str = requests.get(url).text
    html = BeautifulSoup(html_str, 'html.parser')

    link_el = html.find('a', class_='fa-file-download-bt')
    link_str_relative = link_el['href'].replace('file-download', 'start-download')
    link_str_absolute = ROOT_URL + link_str_relative

    _save_file(link_str_absolute, dest)


def _save_file(url, dest):
    with requests.get(url, stream=True) as r:
        filename = re.findall('filename="(.+?)"', r.headers['content-disposition'])[0]
        filepath = os.path.join(dest, filename)
        with open(filepath, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

    filepath_without_ext = '.'.join(filepath.split('.')[:-1])
    os.makedirs(filepath_without_ext, exist_ok=True)
    Archive(filepath).extractall(filepath_without_ext)

    os.remove(filepath)


def _report_fail(url):
    try:
        with open('log.txt', mode='a') as f:
            f.write(url)
            f.write('\n')
    except:
        print('Cannot report fail to log.txt')
        traceback.print_exc()


if __name__ == '__main__':
    try:
        assert len(os.sys.argv) >= 3
        url = os.sys.argv[1]
        dest = os.sys.argv[2]
    except AssertionError:
        print('USAGE: python3 download_file.py URL DEST')
        exit(1)

    download_file(url, dest)

