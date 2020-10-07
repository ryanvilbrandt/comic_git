import os
from configparser import RawConfigParser


def get_comic_url(comic_info: RawConfigParser):
    comic_domain, base_directory = None, ""
    if os.path.isfile("CNAME"):
        with open("CNAME") as f:
            comic_domain = f.read().strip('/')
    elif "GITHUB_REPOSITORY" in os.environ:
        repo_author, base_directory = os.environ["GITHUB_REPOSITORY"].split("/")
        comic_domain = f"{repo_author}.github.io"
    else:
        if comic_info.has_option("Comic Settings", "Comic domain"):
            comic_domain = comic_info.get("Comic Settings", "Comic domain").strip("/")
        else:
            raise ValueError(
                'Set "Comic domain" in the [Comic Settings] section of your comic_info.ini file '
                'before building your site locally. Please see the comic_git wiki for more information.'
            )
        if comic_info.has_option("Comic Settings", "Comic subdirectory"):
            base_directory = comic_info.get("Comic Settings", "Comic subdirectory").strip("/")
    if not comic_domain.startswith("http"):
        if (comic_info.has_option("Comic Settings", "Use https when building comic URL") and
                comic_info.getboolean("Comic Settings", "Use https when building comic URL")):
            comic_domain = "https://" + comic_domain
        else:
            comic_domain = "http://" + comic_domain
    if base_directory:
        base_directory = "/" + base_directory
    comic_url = comic_domain + base_directory
    print(f"Base URL: {comic_url}, base subdirectory: {base_directory}")
    return comic_url, base_directory
