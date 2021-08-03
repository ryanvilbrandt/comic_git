import argparse
import html
import os
import re
import shutil
from collections import OrderedDict, defaultdict
from configparser import RawConfigParser
from copy import deepcopy
from datetime import datetime
from glob import glob
from json import dumps
from time import strptime, time, strftime
from typing import Dict, List, Tuple

from PIL import Image
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from markdown2 import Markdown
from pytz import timezone

from build_rss_feed import build_rss_feed
from utils import get_comic_url

VERSION = "0.2.2"

AUTOGENERATE_WARNING = """<!--
!! DO NOT EDIT THIS FILE !!
It is auto-generated and any work you do here will be replaced the next time this page is generated.
If you want to edit any of these files, edit their *.tpl versions in src/templates.
-->
"""
BASE_DIRECTORY = ""
MARKDOWN = Markdown(extras=["strike"])


def web_path(rel_path: str):
    if rel_path.startswith("/"):
        return BASE_DIRECTORY + rel_path
    return rel_path


def str_to_list(s, delimiter=","):
    """
    split(), but with extra stripping of white space and leading/trailing delimiters
    :param s:
    :param delimiter:
    :return:
    """
    if not s:
        return []
    return [item.strip(" ") for item in s.strip(delimiter + " ").split(delimiter)]


def delete_output_file_space(comic_info: RawConfigParser = None):
    shutil.rmtree("comic", ignore_errors=True)
    if os.path.isfile("feed.xml"):
        os.remove("feed.xml")
    if comic_info is None:
        comic_info = read_info("your_content/comic_info.ini")
    for page in get_pages_list(comic_info):
        if page["template_name"] == "index":
            if os.path.exists("index.html"):
                os.remove("index.html")
        elif page["template_name"] == "404":
            if os.path.exists("404.html"):
                os.remove("404.html")
        else:
            if os.path.exists(page["template_name"]):
                shutil.rmtree(page["template_name"])
    for comic in get_extra_comics_list(comic_info):
        if os.path.exists(comic):
            shutil.rmtree(comic)


def setup_output_file_space(comic_info: RawConfigParser):
    # Clean workspace, i.e. delete old files
    delete_output_file_space(comic_info)


def read_info(filepath, to_dict=False):
    with open(filepath) as f:
        info_string = f.read()
    if not re.search(r"^\[.*?]", info_string):
        # print(filepath + " has no section")
        info_string = "[DEFAULT]\n" + info_string
    info = RawConfigParser()
    info.optionxform = str
    info.read_string(info_string)
    if to_dict:
        # TODO: Support multiple sections
        if not list(info.keys()) == ["DEFAULT"]:
            raise NotImplementedError("Configs with multiple sections not yet supported")
        return dict(info["DEFAULT"])
    return info


def get_option(comic_info: RawConfigParser, section: str, option: str, option_type: type=str, default: str=None) -> str:
    if comic_info.has_section(section):
        if comic_info.has_option(section, option):
            if option_type == str:
                return comic_info.get(section, option)
            if option_type == int:
                return comic_info.getint(section, option)
            if option_type == float:
                return comic_info.getfloat(section, option)
            if option_type == bool:
                return comic_info.getboolean(section, option)
    return default


def get_links_list(comic_info: RawConfigParser):
    link_list = []
    for option in comic_info.options("Links Bar"):
        link_list.append({"name": option, "url": web_path(comic_info.get("Links Bar", option))})
    return link_list


def get_pages_list(comic_info: RawConfigParser, section_name="Pages"):
    if comic_info.has_section("Pages"):
        return [{"template_name": option, "title": web_path(comic_info.get(section_name, option))}
                for option in comic_info.options(section_name)]
    return []


def get_extra_comics_list(comic_info: RawConfigParser) -> List[str]:
    if comic_info.has_option("Comic Settings", "Extra comics"):
        return str_to_list(comic_info.get("Comic Settings", "Extra comics"))
    return []


def build_and_publish_comic_pages(comic_url: str, comic_folder: str, comic_info: RawConfigParser, 
                                  delete_scheduled_posts: bool, processing_times: list):
    page_info_list, scheduled_post_count = get_page_info_list(comic_folder, comic_info, delete_scheduled_posts)
    print([p["page_name"] for p in page_info_list])
    processing_times.append((f"Get info for all pages in '{comic_folder}'", time()))

    # Save page_info_list.json file for use by other pages
    save_page_info_json_file(comic_folder, page_info_list, scheduled_post_count)
    processing_times.append((f"Save page_info_list.json file in '{comic_folder}'", time()))

    # Build full comic data dicts, to build templates with
    comic_data_dicts = build_comic_data_dicts(comic_folder, comic_info, page_info_list)
    processing_times.append((f"Build full comic data dicts for '{comic_folder}'", time()))

    # Create low-res and thumbnail versions of all the comic pages
    process_comic_images(comic_info, comic_data_dicts)
    processing_times.append((f"Process comic images in '{comic_folder}'", time()))

    # Write page info to comic HTML pages
    global_values = {
        "autogenerate_warning": AUTOGENERATE_WARNING,
        "version": VERSION,
        "comic_title": comic_info.get("Comic Info", "Comic name"),
        "comic_author": comic_info.get("Comic Info", "Author"),
        "comic_description": comic_info.get("Comic Info", "Description"),
        "theme": get_option(comic_info, "Comic Settings", "Theme", default="default"),
        "comic_url": comic_url,
        "base_dir": BASE_DIRECTORY,
        "comic_base_dir": f"{BASE_DIRECTORY}/{comic_folder}".rstrip("/"),  # e.g. /base_dir/extra_comic
        "links": get_links_list(comic_info),
        "use_images_in_navigation_bar": comic_info.getboolean("Comic Settings", "Use images in navigation bar"),
        "use_thumbnails": comic_info.getboolean("Archive", "Use thumbnails"),
        "storylines": get_storylines(comic_data_dicts),
        "google_analytics_id": get_option(comic_info, "Google Analytics", "Tracking ID", default="")
    }
    write_html_files(comic_folder, comic_info, comic_data_dicts, global_values)
    processing_times.append((f"Write HTML files for '{comic_folder}'", time()))
    return comic_data_dicts


def get_page_info_list(comic_folder: str, comic_info: RawConfigParser, delete_scheduled_posts: bool) \
        -> Tuple[List[Dict], int]:
    date_format = comic_info.get("Comic Settings", "Date format")
    tzinfo = timezone(comic_info.get("Comic Settings", "Timezone"))
    local_time = datetime.now(tz=tzinfo)
    print(f"Local time is {local_time}")
    page_info_list = []
    scheduled_post_count = 0
    for page_path in glob(f"your_content/{comic_folder}comics/*/"):
        page_info = read_info(f"{page_path}info.ini", to_dict=True)
        post_date = tzinfo.localize(datetime.strptime(page_info["Post date"], date_format))
        if post_date > local_time:
            scheduled_post_count += 1
            # Post date is in the future, so delete the folder with the resources
            if delete_scheduled_posts:
                print(f"Deleting {page_path}")
                shutil.rmtree(page_path)
        else:
            page_info["page_name"] = os.path.basename(os.path.normpath(page_path))
            page_info["Storyline"] = page_info.get("Storyline", "")
            page_info["Characters"] = str_to_list(page_info.get("Characters", ""))
            page_info["Tags"] = str_to_list(page_info.get("Tags", ""))
            page_info_list.append(page_info)

    page_info_list = sorted(
        page_info_list,
        key=lambda x: (strptime(x["Post date"], date_format), x["page_name"])
    )
    return page_info_list, scheduled_post_count


def save_page_info_json_file(comic_folder: str, page_info_list: List, scheduled_post_count: int):
    d = {
        "page_info_list": page_info_list,
        "scheduled_post_count": scheduled_post_count
    }
    os.makedirs(f"{comic_folder}comic", exist_ok=True)
    with open(f"{comic_folder}comic/page_info_list.json", "w") as f:
        f.write(dumps(d))


def get_ids(comic_list: List[Dict], index):
    first_id = comic_list[0]["page_name"]
    last_id = comic_list[-1]["page_name"]
    return {
        "first_id": first_id,
        "previous_id": first_id if index == 0 else comic_list[index - 1]["page_name"],
        "current_id": comic_list[index]["page_name"],
        "next_id": last_id if index == (len(comic_list) - 1) else comic_list[index + 1]["page_name"],
        "last_id": last_id
    }


def get_transcripts(comic_folder: str, comic_info: RawConfigParser, page_name: str) -> OrderedDict:
    if not comic_info.getboolean("Transcripts", "Enable transcripts"):
        return OrderedDict()
    transcripts = OrderedDict()
    transcripts_dir = get_option(
        comic_info, "Transcripts", "Transcripts folder", default=f"your_content/{comic_folder}comics"
    )
    for path in glob(os.path.join(transcripts_dir, page_name, "*.txt")):
        if path.endswith("post.txt"):
            continue
        language = os.path.splitext(os.path.basename(path))[0]
        with open(path, "rb") as f:
            transcripts[language] = f.read().decode("utf-8").replace("\n", "<br>\n")
    default_language = comic_info.get("Transcripts", "Default language")
    if default_language and default_language in transcripts:
        transcripts.move_to_end(default_language, last=False)
    return transcripts


def create_comic_data(comic_folder: str, comic_info: RawConfigParser, page_info: dict,
                      first_id: str, previous_id: str, current_id: str, next_id: str, last_id: str):
    print("Building page {}...".format(page_info["page_name"]))
    page_dir = f"your_content/{comic_folder}comics/{page_info['page_name']}/"
    archive_post_date = strftime(comic_info.get("Archive", "Date format"),
                                 strptime(page_info["Post date"], comic_info.get("Comic Settings", "Date format")))
    post_html = []
    post_text_paths = [
        "your_content/before post text.txt",
        page_dir + "post.txt",
        "your_content/after post text.txt"
    ]
    for path in post_text_paths:
        if os.path.exists(path):
            with open(path, "rb") as f:
                post_html.append(f.read().decode("utf-8"))
    post_html = MARKDOWN.convert("\n\n".join(post_html))
    return {
        "page_name": page_info["page_name"],
        "filename": page_info["Filename"],
        "comic_path": page_dir + page_info["Filename"],
        "thumbnail_path": os.path.join(page_dir, "thumbnail.jpg"),
        "alt_text": html.escape(page_info["Alt text"]),
        "first_id": first_id,
        "previous_id": previous_id,
        "current_id": current_id,
        "next_id": next_id,
        "last_id": last_id,
        "page_title": page_info["Title"],
        "post_date": page_info["Post date"],
        "archive_post_date": archive_post_date,
        "storyline": None if "Storyline" not in page_info else page_info["Storyline"],
        "characters": page_info["Characters"],
        "tags": page_info["Tags"],
        "post_html": post_html,
        "transcripts": get_transcripts(comic_folder, comic_info, page_info["page_name"])
    }


def build_comic_data_dicts(comic_folder: str, comic_info: RawConfigParser, page_info_list: List[Dict]) -> List[Dict]:
    comic_data_dicts = []
    for i, page_info in enumerate(page_info_list):
        comic_dict = create_comic_data(comic_folder, comic_info, page_info, **get_ids(page_info_list, i))
        comic_data_dicts.append(comic_dict)
    return comic_data_dicts


def resize(im, size):
    if "," in size:
        # Convert a string of the form "100, 36" into a 2-tuple of ints (100, 36)
        x, y = size.strip().split(",")
        new_size = (int(x.strip()), int(y.strip()))
    elif size.endswith("%"):
        # Convert a percentage (50%) into a new size (50, 18)
        size = float(size.strip().strip("%"))
        size = size / 100
        x, y = im.size
        new_size = (int(x * size), int(y * size))
    else:
        raise ValueError("Unknown resize value: {!r}".format(size))
    return im.resize(new_size)


def save_image(im, path):
    try:
        # If saving as JPEG, force convert to RGB first
        if path.lower().endswith("jpg") or path.lower().endswith("jpeg"):
            if im.mode != 'RGB':
                im = im.convert('RGB')
        im.save(path)
    except OSError as e:
        if str(e) == "cannot write mode RGBA as JPEG":
            # Get rid of transparency
            bg = Image.new("RGB", im.size, "WHITE")
            bg.paste(im, (0, 0), im)
            bg.save(path)
        else:
            raise


def process_comic_image(comic_info, comic_page_path):
    section = "Image Reprocessing"
    comic_page_dir = os.path.dirname(comic_page_path)
    comic_page_name, comic_page_ext = os.path.splitext(os.path.basename(comic_page_path))
    with open(comic_page_path, "rb") as f:
        im = Image.open(f)
        thumbnail_path = os.path.join(comic_page_dir, "thumbnail.jpg")
        if comic_info.getboolean(section, "Overwrite existing images") or not os.path.isfile(thumbnail_path):
            print(f"Creating thumbnail for {comic_page_name}")
            thumb_im = resize(im, comic_info.get(section, "Thumbnail size"))
            save_image(thumb_im, thumbnail_path)


def process_comic_images(comic_info: RawConfigParser, comic_data_dicts: List[Dict]):
    section = "Image Reprocessing"
    if comic_info.getboolean(section, "Create thumbnails"):
        for comic_data in comic_data_dicts:
            process_comic_image(comic_info, comic_data["comic_path"])


def get_storylines(comic_data_dicts: List[Dict]) -> OrderedDict:
    # Start with an OrderedDict, so we can easily drop the pages we encounter in the proper buckets, while keeping
    # their proper order
    storylines_dict = OrderedDict()
    for comic_data in comic_data_dicts:
        storyline = comic_data["storyline"]
        if not storyline:
            storyline = "Uncategorized"
        if storyline not in storylines_dict.keys():
            storylines_dict[storyline] = []
        storylines_dict[storyline].append(comic_data.copy())
    if "Uncategorized" in storylines_dict:
        storylines_dict.move_to_end("Uncategorized")
    return storylines_dict


def write_html_files(comic_folder: str, comic_info: RawConfigParser, comic_data_dicts: List[Dict], global_values: Dict):
    # Load Jinja environment
    template_folders = ["src/templates"]
    theme = get_option(comic_info, "Comic Settings", "Theme")
    if theme:
        template_folders.insert(0, f"your_content/themes/{theme}/templates")
    print(f"Template folders: {template_folders}")
    jinja_environment = Environment(loader=FileSystemLoader(template_folders))
    # Write individual comic pages
    print("Writing {} comic pages...".format(len(comic_data_dicts)))
    for comic_data_dict in comic_data_dicts:
        html_path = f"{comic_folder}comic/{comic_data_dict['page_name']}/index.html"
        comic_data_dict.update(global_values)
        write_to_template(jinja_environment, "comic.tpl", html_path, comic_data_dict)
    write_other_pages(jinja_environment, comic_folder, comic_info, comic_data_dicts)


def write_other_pages(jinja_environment, comic_folder: str, comic_info: RawConfigParser, comic_data_dicts: List[Dict]):
    last_comic_page = comic_data_dicts[-1]
    pages_list = get_pages_list(comic_info)
    for page in pages_list:
        if page["template_name"] == "tagged":
            write_tagged_pages(jinja_environment, comic_data_dicts)
            continue
        template_name = page["template_name"] + ".tpl"
        if page["template_name"].lower() in ("index", "404"):
            html_path = f"{page['template_name']}.html"
        else:
            html_path = os.path.join(page['template_name'], "index.html")
        if comic_folder:
            html_path = os.path.join(comic_folder, html_path)
        data_dict = {}
        data_dict.update(last_comic_page)
        if page["title"]:
            data_dict["page_title"] = page["title"]
        print("Writing {}...".format(html_path))
        write_to_template(jinja_environment, template_name, html_path, data_dict)


def write_tagged_pages(jinja_environment, comic_data_dicts: List[Dict]):
    last_comic_page = comic_data_dicts[-1]
    tags = defaultdict(list)
    for page in comic_data_dicts:
        for character in page["characters"]:
            tags[character].append(page)
        for tag in page["tags"]:
            tags[tag].append(page)
    for tag, pages in tags.items():
        print("Writing tagged page for {}...".format(tag))
        data_dict = {
            "tag": tag,
            "tagged_pages": pages
        }
        data_dict.update(last_comic_page)
        write_to_template(jinja_environment, "tagged.tpl", f"tagged/{tag}/index.html", data_dict)


def write_to_template(jinja_environment, template_path, html_path, data_dict=None):
    try:
        template = jinja_environment.get_template(template_path)
    except TemplateNotFound:
        file_contents = None
    else:
        if data_dict is None:
            data_dict = {}
        file_contents = template.render(**data_dict)

    if file_contents is None:
        # Check for HTML file and publish that instead
        html_file = f"src/templates/{template_path[:-4]}.html"
        if os.path.isfile(html_file):
            with open(html_file, "rb") as f:
                file_contents = f.read().decode("utf-8")
        else:
            raise FileNotFoundError(f"Template file {template_path} not found")

    dir_name = os.path.dirname(html_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(html_path, "wb") as f:
        f.write(bytes(file_contents, "utf-8"))


def get_extra_comic_info(folder_name: str, comic_info: RawConfigParser):
    # Load the extra comic's comic_info.ini separately so we can make sure to overwrite
    # the Pages and Links List sections completely
    extra_comic_info = RawConfigParser()
    extra_comic_info.read(f"your_content/{folder_name}/comic_info.ini")
    comic_info = deepcopy(comic_info)
    # Always delete existing Pages section; by default, extra comic provides no additional pages
    del comic_info["Pages"]
    # Delete "Links Bar" from original if the extra comic's info has those sections defined
    if "Links Bar" in extra_comic_info:
        del comic_info["Links Bar"]
    # Read the extra comic info in again, to merge with the original comic info
    comic_info.read(f"your_content/{folder_name}/comic_info.ini")
    return comic_info


def print_processing_times(processing_times: List[Tuple[str, float]]):
    last_processed_time = None
    print("")
    for name, t in processing_times:
        if last_processed_time is not None:
            print("{}: {:.2f} ms".format(name, (t - last_processed_time) * 1000))
        last_processed_time = t
    print("{}: {:.2f} ms".format("Total time", (processing_times[-1][1] - processing_times[0][1]) * 1000))


def main(delete_scheduled_posts=False):
    global BASE_DIRECTORY
    processing_times = [("Start", time())]

    # Get site-wide settings for this comic
    comic_info = read_info("your_content/comic_info.ini")
    comic_url, BASE_DIRECTORY = get_comic_url(comic_info)

    processing_times.append(("Get comic settings", time()))

    # Setup output file space
    setup_output_file_space(comic_info)
    processing_times.append(("Setup output file space", time()))

    if not delete_scheduled_posts and comic_info.has_option("Comic Settings", "Delete scheduled posts"):
        delete_scheduled_posts = comic_info.getboolean("Comic Settings", "Delete scheduled posts")

    # Build and publish pages for main comic
    print("Main comic")
    comic_data_dicts = build_and_publish_comic_pages(comic_url, "", comic_info, delete_scheduled_posts, 
                                                     processing_times)

    # Build RSS feed
    build_rss_feed(comic_info, comic_data_dicts)
    processing_times.append(("Build RSS feed", time()))

    # Build any extra comics that may be needed
    for extra_comic in get_extra_comics_list(comic_info):
        print(extra_comic)
        extra_comic_info = get_extra_comic_info(extra_comic, comic_info)
        os.makedirs(extra_comic, exist_ok=True)
        build_and_publish_comic_pages(comic_url, extra_comic.strip("/") + "/", extra_comic_info, 
                                      delete_scheduled_posts, processing_times)

    print_processing_times(processing_times)


def parse_args():
    parser = argparse.ArgumentParser(description='Manual build of comic_git')
    parser.add_argument("-d", "--delete-scheduled-posts", action="store_true", help="Deletes scheduled post content "
                        "when the script is run. USE AT YOUR OWN RISK! You can discard your changes in GitHub Desktop "
                        "if you accidentally delete important files.")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(args.delete_scheduled_posts)
