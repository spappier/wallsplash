#!/usr/bin/env python2

import subprocess
import urlparse
import os
import re

import requests

BASE_URL = 'https://source.unsplash.com/random/1280x800'
WALLPAPER_SIZE = '1280x800'
IMAGES_FOLDER = '/tmp'


def download_wallpaper(url):
    r = requests.get(url, stream=True)
    r.raise_for_status()
    url_data = urlparse.urlparse(url)
    image_path = os.path.join(IMAGES_FOLDER, url_data.path.split('/')[-1])
    with open(image_path, 'wb') as f:
        for chunk in r:
            f.write(chunk)
    return image_path


def get_wallpaper_url():
    r = requests.get(BASE_URL, allow_redirects=False)
    r.raise_for_status()
    if not r.is_redirect:
        print('not a redirect')
        raise SystemExit(1)
    return r.headers.get('location')


def set_wallpaper(fn):
    subprocess.call(['gsettings', 'set', 'org.gnome.desktop.background',
                     'picture-uri', fn])


def main():
    url = get_wallpaper_url()
    fn = download_wallpaper(url)
    set_wallpaper(fn)


if __name__ == '__main__':
    main()
