from glob import glob
from json import loads
from os.path import basename, isfile
from os.path import join as pjoin
from re import sub
from time import strptime, strftime
from urllib.parse import urljoin
from xml.dom import minidom
from xml.etree import ElementTree


DATE_FORMAT = "%B %d, %Y"

cdata_dict = {}


def get_comic_data(path):
    info_json_path = pjoin(path, "info.json")
    post_html_path = pjoin(path, "post.html")
    if not isfile(info_json_path):
        print("Found no info.json file in " + path)
        return None, None
    with open(info_json_path) as f:
        info_json = loads(f.read())
    if isfile(post_html_path):
        with open(post_html_path, "rb") as f:
            post_html = f.read().decode("utf-8")
    else:
        post_html = ""
    return info_json, post_html


def add_item(xml_parent, info_json, post_html, post_id, creator, comic_url):
    global cdata_dict
    item = ElementTree.SubElement(xml_parent, "item")
    ElementTree.SubElement(item, "title").text = info_json["title"]
    ElementTree.SubElement(item, "dc:creator").text = creator
    post_date = strptime(info_json["post_date"], DATE_FORMAT)
    ElementTree.SubElement(item, "pubDate").text = strftime("%a, %d %b %Y %H:%M:%S +0000", post_date)
    direct_link = urljoin(comic_url, "index.html") + "?id=" + str(post_id)
    ElementTree.SubElement(item, "link").text = direct_link
    ElementTree.SubElement(item, "guid", isPermaLink="true").text = direct_link
    for tag in info_json["tags"]:
        ElementTree.SubElement(item, "category").text = tag
    comic_image_url = urljoin(comic_url, "your_content/comics/{}/{}".format(post_id, info_json["filename"]))
    html = '<p><img src="{}"'.format(comic_image_url)
    if info_json.get("alt_text"):
        html += ' alt_text="{}"'.format(info_json["alt_text"].replace(r'"', r'\"'))
    html += "></p>\n\n<hr>\n\n"
    html += post_html
    # print(html)
    cdata_dict["post_id_" + post_id] = "<![CDATA[{}]]>".format(html)
    ElementTree.SubElement(item, "description").text = "{post_id_" + post_id + "}"


def pretty_xml(element):
    raw_string = ElementTree.tostring(element).decode("utf-8")
    flattened_string = sub(r"\n\s*", "", raw_string)
    pretty_string = minidom.parseString(flattened_string).toprettyxml(indent="    ")
    # print(pretty_string)
    # return bytes(pretty_string.replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"').replace(r"\n", "\n"), "utf-8")
    return pretty_string


def main():
    global cdata_dict
    tree = ElementTree.parse("feed_base.xml")
    root = tree.getroot()
    channel = root.find("channel")
    creator = channel.find("{http://purl.org/dc/elements/1.1/}creator").text
    comic_url = channel.find("link").text

    for path in glob("../../your_content/comics/*"):
        info_json, post_html = get_comic_data(path)
        if info_json is None:
            continue
        post_id = basename(path)
        add_item(channel, info_json, post_html, post_id, creator, comic_url)

    pretty_string = pretty_xml(root)

    # Replace CDATA manually, because XML is stupid and I can't figure out how to insert raw text
    pretty_string = pretty_string.format(**cdata_dict)

    with open("../../feed.xml", 'wb') as f:
        f.write(bytes(pretty_string, "utf-8"))


if __name__ == "__main__":
    main()
