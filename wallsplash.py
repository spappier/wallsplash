#!/usr/bin/env python

'''
Wallsplash

Usage:
  wallsplash ( [--category=<category>] | [--user=<user>] ) [--query=<query>]
  wallsplash save
  wallsplash --version
  wallsplash -h | --help

Options:
  --category=<category>  Category to pull from.
  --user=<user>          User to pull from.
  --query=<query>        Comma-separated search terms.
  --version              Show version.
  -h --help              Show this screen.
'''

from __future__ import print_function

import subprocess
import shutil
import time
import os

import requests
import docopt

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

BASE_URL = 'https://source.unsplash.com'
WALLPAPER_SIZE = '1280x800'
WALLPAPER_FILE = 'current-wallpaper'
IMAGES_FOLDER = '/tmp'
IMAGES_FOLDER_SAVE = 'Pictures'
CATEGORIES = ('buildings', 'food', 'nature', 'people', 'technology', 'objects')


def download_wallpaper(url):
    r = requests.get(url, stream=True)
    r.raise_for_status()
    url_data = urlparse.urlparse(url)
    image_path = os.path.join(IMAGES_FOLDER, WALLPAPER_FILE)
    with open(image_path, 'wb') as f:
        for chunk in r:
            f.write(chunk)
    return image_path


def get_wallpaper_url(resource, query=None):
    params = {'': query} if query else None
    r = requests.get('{}/{}/{}'.format(BASE_URL, resource, WALLPAPER_SIZE),
                     params=params, allow_redirects=False)
    r.raise_for_status()
    if not r.is_redirect:
        print('not a redirect')
        raise SystemExit(1)
    return r.headers.get('location')


def set_wallpaper(fn):
    subprocess.call(['gsettings', 'set', 'org.gnome.desktop.background',
                     'picture-uri', fn])


def switch_wallpaper(category=None, user=None, query=None):
    if category:
        if category not in CATEGORIES:
            print('category should be one of: {}'.format(', '.join(CATEGORIES)))
            raise SystemExit(1)
        resource = 'category/{}'.format(category)
    elif user:
        resource = 'user/{}'.format(user)
    else:
        resource = 'random'
    url = get_wallpaper_url(resource, query=query)
    fn = download_wallpaper(url)
    set_wallpaper(fn)


def save_current():
    image_path = os.path.join(IMAGES_FOLDER, WALLPAPER_FILE)
    home = os.path.expanduser("~")
    current_millis = str(int(round(time.time() * 1000)))
    image_save_destination = os.path.join(home, IMAGES_FOLDER_SAVE, WALLPAPER_FILE + "-" + current_millis)
    shutil.copyfile(image_path, image_save_destination)
    set_wallpaper(image_save_destination)
    print('saved to: {}'.format(image_save_destination))


def main():
    args = docopt.docopt(__doc__, version='0.1.1')
    if args.get('save'):
        save_current()
    else:
        switch_wallpaper(
            args.get('--category'),
            args.get('--user'),
            args.get('--query')
        )

if __name__ == '__main__':
    main()
