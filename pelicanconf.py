#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = '71e6fd52'
SITENAME = "71e6fd52's blog"

PATH = 'content'

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = 'zh'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
# LINKS = (('Pelican', 'http://getpelican.com/'),
         # ('Python.org', 'http://python.org/'),
         # ('Jinja2', 'http://jinja.pocoo.org/'),
         # ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (
    ('github', 'https://github.com/71e6fd52'),
    ('twitter', 'https://twitter.com/71e6fd52'),
    ('mail-s', 'mailto:71e6fd52@gmail.com'),
)

TWITTER_USERNAME = '71e6fd52'

DEFAULT_PAGINATION = 20

STATIC_PATHS = [
    'images',
    'extra',
]
EXTRA_PATH_METADATA = {
    'extra/favicon.ico': {'path': 'favicon.ico'},
}

FAVICON = 'favicon.ico'

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

THEME = 'theme'

PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = ['summary', 'neighbors']

DISPLAY_PAGES_ON_MENU = True
DISPLAY_SUMMARY = True
SUMMARY_USE_FIRST_PARAGRAPH = True
