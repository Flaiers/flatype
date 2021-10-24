#!/usr/bin/env python
import os

import django

import packs


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

django.setup()

'''Rename tables in database'''
packs.rename_tables()
