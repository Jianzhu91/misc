#! /usr/bin/env python
# -*- coding: utf-8 -*
"""Name---Jian Zhu"""


import sys

# reducer.py: the reducer programme that filter the logs whose 
# total views are over 100000

current_title = None
title = None
value = None
current_month_count = [0] * 31
total = 0



for line in sys.stdin:
    line = line.strip()
    date = 32
    title, value = line.split('\t', 1)
    count, time = value.split('-', 1)

    try:
        count = int(count)
        date = int(time[-2:])
    except ValueError:
        continue
    # If the coming in article is the current article
    if current_title == title:
        current_month_count[date-1] += count
    # A new article comes in
    else:
        if current_title:
            # Print the current article to the STDOUT
            total = sum(current_month_count)
            if total > 100000:
                str_out = str(total) + '\t' + current_title
                single_day = 1
                while single_day < 32:
                    if single_day < 10:
                        str_out += '\t' + '2015080' + str(single_day) + ':' + str(current_month_count[single_day-1])
                    else:
                        str_out += '\t' + '201508' + str(single_day) + ':' + str(current_month_count[single_day-1])
                    single_day += 1
                print str_out
        
        # a new log comes in
        current_title = title
        current_month_count = [0] * 31
        current_month_count[date-1] += count
        total = 0


# print the last log if necessary
if current_title == title:
    total = sum(current_month_count)
    if total > 100000:
        str_out = str(total) + '\t' + current_title
        single_day = 1
        while single_day < 32:
            if single_day < 10:
                str_out += '\t' + '2015080' + str(single_day) + ':' + str(current_month_count[single_day-1])
            else:
                str_out += '\t' + '201508' + str(single_day) + ':' + str(current_month_count[single_day-1])
            single_day += 1
        print str_out
