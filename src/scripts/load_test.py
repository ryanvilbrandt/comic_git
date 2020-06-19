"""
A script for generating a LOT of comic folders and their info.json,
intended for load testing the archive and tagged pages
"""

from datetime import datetime, timedelta
from os import makedirs
from shutil import copyfile

for i in range(1, 101):
    folder_name = f"Page {i}"
    post_date = (datetime(2019, 1, 1) + timedelta(i - 1)).strftime("%B %d, %Y")
    chapter_num = int((i - 1) / 20) + 1
    makedirs("../../your_content/comics/" + folder_name)

    text = f"""
Title = Page {i}
Post date = {post_date}
Filename = Page_197.png
Alt text = 
Storyline = Chapter {chapter_num}
"""
    with open("../../your_content/comics/" + folder_name + "/info.ini", 'w') as f:
        f.write(text)
    copyfile("Page_197.png", "../../your_content/comics/" + folder_name + "/Page_197.png")
