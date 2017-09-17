#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = 'https://blog.71e6fd52.ml'
RELATIVE_URLS = False

FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'

DELETE_OUTPUT_DIRECTORY = True

MENUITEMS = (('Blog', SITEURL),)

THEME = 'theme'

DISPLAY_PAGES_ON_MENU = True

DISQUS_SITENAME = ;'71e6fd52s-blog'
UYAN_UID = 2144797
GITMENT_OWNER = '71e6fd52'
GITMENT_REPO = 'blog'
GITMENT_ID = 'cc78bf6b5758fd53a38a'
GITMENT_SECRET = '96acad33ae8646e60b8f0bfd7d1c99e24f7a7caf'
#GOOGLE_ANALYTICS = ""
