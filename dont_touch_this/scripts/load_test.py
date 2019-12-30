"""
A script for generating a LOT of comic folders and their info.json,
intended for load testing the archive and tagged pages
"""

from datetime import datetime, timedelta
from json import dumps
from os import makedirs

for i in range(1, 196):
    folder_name = "{:>03}".format(i)
    post_date = (datetime(2019, 1, 1) + timedelta(i - 1)).strftime("%B %d, %Y")
    makedirs(folder_name)
    json = {
        "title": "Page {}".format(i),
        "post_date": post_date,
        "tags": ["Tag {}".format(n) for n in range(i, i + 5)]
    }
    with open("../../your_content/comics/" + folder_name + "/info.json", 'w') as f:
        f.write(dumps(json, indent=4))
