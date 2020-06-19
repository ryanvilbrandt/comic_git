import glob
import os
import shutil
import time
from collections import defaultdict
from urllib.request import urlretrieve
from xml.etree import ElementTree as ET



WEBCOMIC_POST_TYPE = "webcomic1"
TRANSCRIPT_POST_TYPE = "webcomic_transcript"


# filename = "tamberlane.WordPress.2020-05-31.xml"
#
# tree = ET.parse(filename)
# root = tree.getroot()
#
# channel = root[0]
#
# pages = defaultdict(dict)
#
# for child in channel.iter('item'):
#     post_type = child.find("{http://wordpress.org/export/1.2/}post_type").text
#     if post_type == WEBCOMIC_POST_TYPE:
#         post_id = child.find('{http://wordpress.org/export/1.2/}post_id').text
#         pages[post_id]["page_name"] = child.find('{http://wordpress.org/export/1.2/}post_name').text
#     elif post_type == TRANSCRIPT_POST_TYPE:
#         parent_id = child.find('{http://wordpress.org/export/1.2/}post_parent').text
#         if "transcripts" not in pages[parent_id]:
#             pages[parent_id]["transcripts"] = {}
#         category = child.find("category")
#         if not category is None:
#             language = child.find("category").text
#             tscript = child.find('{http://purl.org/rss/1.0/modules/content/}encoded').text
#             pages[parent_id]["transcripts"][language] = tscript
#
#
# for post_id, page in pages.items():
#     for k in ["page_name", "transcripts"]:
#         if k not in page:
#             print(page)
#             break
#     else:
#         dir_name = f"../../your_content/transcripts/{page['page_name']}"
#         os.makedirs(dir_name, exist_ok=True)
#         for lang, tscript in page["transcripts"].items():
#             # if lang == "English":
#             #     filename = "en"
#             # elif lang == "Español":
#             #     filename = "es"
#             # elif lang == "Français":
#             #     filename = "fr"
#             # elif lang == "Deutsch":
#             #     filename = "de"
#             # elif lang == "Pусский":
#             #     filename = "ru"
#             # else:
#             filename = lang
#             filepath = f"{dir_name}/{filename}.txt"
#             while os.path.exists(filepath):
#                 filepath += "1"
#             with open(filepath, "wb") as f:
#                 f.write(tscript.encode("utf-8"))

print("")
folders = glob.glob("../../your_content/transcripts/*")
# print(folders)
for i in range(1, 219):
    if f"../../your_content/transcripts\\page-{i}" not in folders:
        print(f"Missing page-{i}")