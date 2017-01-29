#! /usr/bin/env python
# -*- coding: utf-8 -*
"""Name---Jian Zhu"""

import os
import sys

# mapper.py: this is the mapper programme for the Wikipedia Project 1.2
# It simply filters the Wikipedia data based on the filter from Project1_1.

results = []
special_pages = set([
    'Media:', 'Special:', 'Talk:', 'User:', 'User_talk:', 'Project:',\
    'Project_talk:', 'File:', 'File_talk:', 'MediaWiki:', 'MediaWiki_talk:',\
    'Template:', 'Template_talk:', 'Help:', 'Help_talk:', 'Category:',\
    'Category_talk:', 'Portal:', 'Wikipedia:', 'Wikipedia_talk:'\
    ])
boilerplate = set([
    '404_error/', 'Main_Page',\
    'Hypertext_Transfer_Protocol', 'Search'\
    ])
image_files = set([
    '.jpg', '.gif', '.png', '.JPG',\
    '.GIF', '.PNG', '.txt', '.ico'\
    ])

filename = os.environ["mapreduce_map_input_file"]
url = filename.split('-')
time = url[2]


for line in sys.stdin:
    line = line.strip()           
    is_special = 0
    is_boilerplate = 0
    is_image = 0
    components = line.split()
    if len(components) < 4:
        continue
    # Step 1
    # if project name is 'en'
    if components[0] != 'en':
        continue
    # Step 2
    # if the page is a special page
    for page in special_pages:
        if components[1].startswith(page):
            is_special = 1
            break
    if is_special == 1:
        continue
    # Step 3
    # if starts with Uppercase letter
    head = components[1][0].upper()
    if head != components[1][0]:
        continue
    # Step 4
    # if it is a image file
    for suffix in image_files:
        if components[1].endswith(suffix):
            is_image = 1
            break
    if is_image == 1:
        continue
    # Step 5
    # if it is a boilerplate page title
    for item in boilerplate:
        if item == components[1]:
            is_boilerplate = 1;
            break
    if is_boilerplate == 1:
        continue
    # Step 6: output the filtered log to the standard output,
    # with the date of each log
    str_out = components[1] + '\t' + components[2] + '-' + time
    print str_out
