import os
from configparser import RawConfigParser


def get_comic_url(comic_info: RawConfigParser):
    comic_domain, base_directory = None, None
    if "GITHUB_REPOSITORY" in os.environ:
        repo_author, base_directory = os.environ["GITHUB_REPOSITORY"].split("/")
        comic_domain = f"http://{repo_author}.github.io"
    if comic_info.has_option("Comic Info", "Comic domain"):
        comic_domain = comic_info.get("Comic Info", "Comic domain").rstrip("/")
    if comic_info.has_option("Comic Info", "Comic subdirectory"):
        base_directory = comic_info.get("Comic Info", "Comic subdirectory").strip("/")
    if not comic_domain or not base_directory:
        raise ValueError(
            'Set "Comic domain" and "Comic subdirectory" in the [Comic Info] section of your comic_info.ini file '
            'before building your site locally. Please see the comic_git wiki for more information.'
        )
    comic_url = comic_domain + '/' + base_directory
    return comic_url, base_directory