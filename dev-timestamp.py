import os
import re

# Location of data
file_name = 'sample.log'

# Our first regular expression
timestamp = re.compile(r'(\d{2}:\d{2}:\d{2}) \(\w+\) TIMESTAMP (\d+/\d+/\d+)')

# Read the data and print the date and time from the TIMESTAMP lines
with open(file_name) as f:
    for line in f:
        if timestamp.match(line):
            p = timestamp.match(line)
            time = p.group(1)
            date = p.group(2)
            print(f"The date and time were:  {date} {time}")
