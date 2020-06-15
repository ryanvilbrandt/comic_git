import glob
import os
import shutil
import time
from collections import defaultdict
from urllib.request import urlretrieve
from xml.etree import ElementTree as ET



WEBCOMIC_POST_TYPE = "webcomic1"
ATTACHMENT_POST_TYPE = "attachment"


# filename = "tamberlane.WordPress.2020-05-31.xml"
filename = "tamberlane.WordPress.2020-06-13.xml"

tree = ET.parse(filename)
root = tree.getroot()

channel = root[0]

pages = defaultdict(dict)

for child in channel.iter('item'):
    # if child.find("title").text in ["Page 1", "Page 2", "Page 3"]:
    #     for c in child:
    #         print(c.tag)
    #         if c.attrib:
    #             print(f"\t{repr(c.attrib)}")
    #         print(f"\t{repr(c.text)}")
    #     print("")

    post_name = child.find('{http://wordpress.org/export/1.2/}post_name').text
    if post_name is None:
        continue
    post_type = child.find("{http://wordpress.org/export/1.2/}post_type").text
    if post_type == WEBCOMIC_POST_TYPE:
        if post_name.endswith("-2"):
            post_name = post_name[:-2]
        pages[post_name]["title"] = child.find('title').text
        pages[post_name]["page_name"] = post_name
        pages[post_name]["post_date"] = child.find('{http://wordpress.org/export/1.2/}post_date').text
        pages[post_name]["text_post"] = child.find('{http://purl.org/rss/1.0/modules/content/}encoded').text
        characters = []
        for c in child.iter("category"):
            if c.attrib["domain"].endswith("storyline"):
                pages[post_name]["storyline"] = c.text
            elif c.attrib["domain"].endswith("character"):
                characters.append(c.text)
            else:
                print("WHAT IS THIS FUCK")
                print(c)
        pages[post_name]["characters"] = characters
    elif post_type == ATTACHMENT_POST_TYPE:
        if post_name.endswith("-2"):
            post_name = post_name[:-2]
        elif post_name.endswith("-3"):
            post_name = post_name[:-2]
        elif post_name.endswith("-ks"):
            post_name = post_name[:-3]
        elif post_name.endswith("-ks2"):
            post_name = post_name[:-4]
        elif post_name.endswith("-ggc"):
            post_name = post_name[:-4]
        post_name = post_name.replace("_", "-")
        pages[post_name]["attachment_name"] = post_name
        pages[post_name]["page_link"] = child.find('{http://wordpress.org/export/1.2/}attachment_url').text
        pages[post_name]["alt_text"] = child.find('{http://wordpress.org/export/1.2/excerpt/}encoded').text
    # else:
    #     print(f"Bad post type {post_type} for {child.find('title').text}")

# for f in glob.glob("../../your_content/comics/*"):
#     shutil.rmtree(f)

for name, page in pages.items():
    if "page_name" in page:
        print(name)
        for k in ["title", "page_name", "post_date", "text_post", "characters", "page_link", "alt_text"]:
            if k not in page:
                print(k)
                print(page)
                break
        else:
            dir_name = f"../../your_content/comics/{name}"
            os.makedirs(dir_name, exist_ok=True)
            page_filename = os.path.basename(page["page_link"])
            page_filepath = dir_name + "/" + page_filename
            if not os.path.isfile(page_filepath):
                urlretrieve(page["page_link"], page_filepath)
            post_date = time.strftime("%B %d, %Y", time.strptime(page["post_date"], "%Y-%m-%d %H:%M:%S"))
            # Build files
            with open(dir_name + "/info.ini", "wb") as f:
                f.write(f"""Title = {page["title"]}
Post date = {post_date}
Filename = {page_filename}
Alt text = {page["alt_text"]}
Storyline = {page.get("storyline", "")}
Characters = {", ".join(page["characters"])}
Tags = """.encode("utf-8"))
            if not page["text_post"]:
                page["text_post"] = ""
            with open(dir_name + "/post.txt", "wb") as f:
                f.write(page["text_post"].encode("utf-8"))


print("")
folders = glob.glob("../../your_content/comics/*")
for i in range(1, 219):
    if f"../../your_content/comics\\page-{i}" not in folders:
        print(f"Missing page-{i}")
