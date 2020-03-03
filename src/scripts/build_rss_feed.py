import os
from configparser import RawConfigParser
from re import sub
from time import strptime, strftime
from typing import List, Dict
from urllib.parse import urljoin
from xml.dom import minidom
from xml.etree import ElementTree
from xml.etree.ElementTree import register_namespace

DATE_FORMAT = "%B %d, %Y"

cdata_dict = {}


def add_base_tags_to_channel(channel, comic_url, comic_info):
    atom_link = ElementTree.SubElement(channel, "{http://www.w3.org/2005/Atom}link")
    atom_link.set("href", urljoin(comic_url, "feed.xml"))
    atom_link.set("rel", "self")
    atom_link.set("type", "application/rss+xml")

    # Set title, description, creator, and language
    ElementTree.SubElement(channel, "title").text = comic_info.get("Comic Info", "Comic name")
    ElementTree.SubElement(channel, "description").text = comic_info.get("RSS Feed", "Description")
    ElementTree.SubElement(channel, "link").text = comic_url
    ElementTree.SubElement(channel, "{http://purl.org/dc/elements/1.1/}creator").text = \
        comic_info.get("Comic Info", "Author")
    ElementTree.SubElement(channel, "language").text = comic_info.get("RSS Feed", "Language")


def add_image_tag(channel, comic_url, comic_info):
    image_tag = ElementTree.SubElement(channel, "image")
    ElementTree.SubElement(image_tag, "title").text = comic_info.get("Comic Info", "Comic name")
    ElementTree.SubElement(image_tag, "link").text = comic_url
    ElementTree.SubElement(image_tag, "url").text = urljoin(comic_url, comic_info.get("RSS Feed", "Image"))
    ElementTree.SubElement(image_tag, "width").text = comic_info.get("RSS Feed", "Image width")
    ElementTree.SubElement(image_tag, "height").text = comic_info.get("RSS Feed", "Image height")


def add_item(xml_parent, comic_data, comic_url, comic_info):
    global cdata_dict
    post_id = comic_data["page_name"]
    item = ElementTree.SubElement(xml_parent, "item")
    ElementTree.SubElement(item, "title").text = comic_data["page_title"]
    ElementTree.SubElement(item, "{http://purl.org/dc/elements/1.1/}creator").text = \
        comic_info.get("Comic Info", "Author")
    post_date = strptime(comic_data["post_date"], comic_info.get("Comic Settings", "Date format"))
    ElementTree.SubElement(item, "pubDate").text = strftime("%a, %d %b %Y %H:%M:%S +0000", post_date)
    direct_link = urljoin(comic_url, "comic/{}.html".format(post_id))
    ElementTree.SubElement(item, "link").text = direct_link
    ElementTree.SubElement(item, "guid", isPermaLink="true").text = direct_link
    for tag in comic_data["tags"]:
        ElementTree.SubElement(item, "category").text = tag
    comic_image_url = urljoin(comic_url, "your_content/comics/{}/{}".format(post_id, comic_data["filename"]))
    html = build_rss_post(comic_image_url, comic_data.get("alt_text"), comic_data["post_html"])
    cdata_dict["post_id_" + post_id] = "<![CDATA[{}]]>".format(html)
    ElementTree.SubElement(item, "description").text = "{post_id_" + post_id + "}"


def build_rss_post(comic_image_url, alt_text, post_html):
    comic_image = '<img src="{}"{}>'.format(
        comic_image_url,
        ' alt_text="{}"'.format(alt_text.replace(r'"', r'\"')) if alt_text else ""
    )
    return "<p>{}</p>\n\n<hr>\n\n{}".format(comic_image, post_html)


def pretty_xml(element):
    raw_string = ElementTree.tostring(
        element, xml_declaration=True, encoding='utf-8', method="xml"
    ).decode("utf-8")
    flattened_string = sub(r"\n\s*", "", raw_string)
    pretty_string = minidom.parseString(flattened_string).toprettyxml(indent="    ")
    # print(pretty_string)
    # return bytes(pretty_string.replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"').replace(r"\n", "\n"), "utf-8")
    return pretty_string


def build_rss_feed(comic_info: RawConfigParser, comic_data_dicts: List[Dict]):
    global cdata_dict

    if not comic_info.getboolean("RSS Feed", "Build RSS feed"):
        return

    if "GITHUB_REPOSITORY" not in os.environ:
        raise ValueError("Set GITHUB_REPOSITORY in your environment variables before building your RSS feed locally")

    register_namespace("atom", "http://www.w3.org/2005/Atom")
    register_namespace("dc", "http://purl.org/dc/elements/1.1/")
    root = ElementTree.Element("rss")
    root.set("version", "2.0")
    channel = ElementTree.SubElement(root, "channel")

    # Build comic URL
    repo_author, repo_name = os.environ["GITHUB_REPOSITORY"].split("/")
    comic_url = "https://{}.github.io/{}/".format(repo_author, repo_name)

    add_base_tags_to_channel(channel, comic_url, comic_info)
    add_image_tag(channel, comic_url, comic_info)

    for comic_data in comic_data_dicts:
        add_item(channel, comic_data, comic_url, comic_info)

    pretty_string = pretty_xml(root)

    # Replace CDATA manually, because XML is stupid and I can't figure out how to insert raw text
    pretty_string = pretty_string.format(**cdata_dict)

    with open("feed.xml", 'wb') as f:
        f.write(bytes(pretty_string, "utf-8"))
