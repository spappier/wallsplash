# -*- coding: utf-8 -*-

import sys
from setuptools import setup

setup_requires = []
if sys.argv[-1] in ('sdist', 'bdist_wheel'):
    setup_requires.append('setuptools-markdown')

setup(
    name='wallsplash',
    author='Santiago Pappier',
    author_email='spappier@gmail.com',
    url='http://github.com/spappier/wallsplash',
    version='1.0',
    description='command line wallpaper downloader / switcher.',
    long_description_markdown_filename='README.md',
    license='MIT',
    entry_points=dict(console_scripts=['wallsplash = wallsplash:main']),
    py_modules=['wallsplash'],
    scripts=['wallsplash.py'],
    install_requires=['requests', 'docopt', 'six'],
    setup_requires=setup_requires,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Utilities',
    ]
)
