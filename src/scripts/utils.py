import os
from configparser import RawConfigParser
from typing import List, Dict

from jinja2 import TemplateNotFound

jinja_environment = None


def get_comic_url(comic_info: RawConfigParser):
    comic_domain, base_directory = None, ""
    # Let user-defined comic domain and base directory override all other values
    if comic_info.has_option("Comic Settings", "Comic domain"):
        comic_domain = comic_info.get("Comic Settings", "Comic domain").strip("/")
    if comic_info.has_option("Comic Settings", "Comic subdirectory"):
        base_directory = comic_info.get("Comic Settings", "Comic subdirectory").strip("/")
    # If we have a CNAME file, use that for the comic domain
    if not comic_domain and os.path.isfile("CNAME"):
        with open("CNAME") as f:
            comic_domain = f.read().strip('/')
    # If this is running in GitHub and the domain and base directory were not user-defined, derive them here
    if "GITHUB_REPOSITORY" in os.environ:
        repo_author, repo_name = os.environ["GITHUB_REPOSITORY"].split("/")
        if not comic_domain:
            comic_domain = f"{repo_author}.github.io"
        if not base_directory:
            base_directory = repo_name
            if base_directory.lower() == f"{repo_author.lower()}.github.io":
                # In this case, Github will try to deploy to http://<username>.github.io/ so we unset base_directory
                base_directory = ""
    # Helpful error for dumb schmucks trying to build locally for the first time
    if not comic_domain:
        raise ValueError(
            'Set "Comic domain" in the [Comic Settings] section of your comic_info.ini file '
            'before building your site locally. Please see the comic_git wiki for more information.'
        )
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


def str_to_list(s: str, delimiter: str=",") -> List[str]:
    """
    split(), but with extra stripping of white space and leading/trailing delimiters
    :param s:
    :param delimiter:
    :return:
    """
    if not s:
        return []
    return [item.strip(" ") for item in s.strip(delimiter + " ").split(delimiter)]


def find_project_root():
    while not os.path.exists("your_content"):
        last_cwd = os.getcwd()
        os.chdir("..")
        if os.getcwd() == last_cwd:
            raise FileNotFoundError("Couldn't find a folder in the path matching 'your_content'. Make sure you're "
                                    "running this script from within the comic_git repository.")


def write_to_template(template_name: str, html_path: str, data_dict: Dict=None) -> None:
    """
    Searches for either an HTML or a TPL file named <template_name> in first the "templates" folder of your
    theme directory, or the /src/templates directory. It then builds that template at the specified <html_path> using
    the given <data_dict> as a list of variables to pass into the template when it's rendered.
 
    :param template_name: The name of the template file or HTML file you wish to load
    :param html_path: The path to write the HTML file, relative to the repository root. If you want it to write to a 
    directory (e.g. ...github.io/comic_git/cool_stuff/), then add index.html file at the end.
    (e.g. "cool_stuff/index.html")
    :param data_dict: The dictionary of values to pass to the template when it's rendered.
    :return: None
    """
    if jinja_environment is None:
        raise RuntimeError("Jinja environment was not initialized before write_to_template was called.")
    try:
        file_contents = jinja_environment.get_template(template_name + ".html").render()
    except TemplateNotFound:
        # If a matching *.html file can't be found, try to find a matching *.tpl file
        try:
            template = jinja_environment.get_template(template_name + ".tpl")
            if data_dict is None:
                data_dict = {}
            file_contents = template.render(**data_dict)
        except TemplateNotFound:
            raise TemplateNotFound(f"Template matching '{template_name}' not found")

    dir_name = os.path.dirname(html_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    print(f"Writing {html_path}")
    with open(html_path, "wb") as f:
        f.write(bytes(file_contents, "utf-8"))
