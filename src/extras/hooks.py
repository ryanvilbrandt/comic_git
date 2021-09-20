import utils


def extra_global_values(comic_folder, comic_info, comic_data_dicts):
    """
    Returns a dictionary of values that will be added to the global values sent to all templates when they're built.

    :param comic_folder: If the main comic is being built, this will be blank. Otherwise, it's the name of the extra
    comic that's currently being built. Use this value if you want to return different global values depending on what
    comic is being built.
    :param comic_info: The comic_info.ini file parsed into a RawConfigParser object.
    :param comic_data_dicts: List of comic data dicts that were built during the previous processing steps.
    :return:
    """
    return {}


def build_other_pages(comic_folder, comic_info, comic_data_dicts):
    """
    This function is called after all other HTML files are built. You can use this function to build whatever
    additional HTML files you may want, using the utils.write_to_template() function.

    :param comic_folder: If the main comic is being built, this will be blank. Otherwise, it's the name of the extra
    comic that's currently being built. Use this value if you want to return different global values depending on what
    comic is being built.
    :param comic_info: The comic_info.ini file parsed into a RawConfigParser object.
    :param comic_data_dicts: List of comic data dicts that were built during the previous processing steps. Each data
    dict also contains the global values passed in to all templates when they're built. 
    :return:
    """
    # You can use comic_data_dicts[-1] to pass the last comic_data_dict to the template so it can have access to all
    # the global template variables.

    # utils.write_to_template("infinite_scroll", "path/to/html/index.html", comic_data_dicts[-1])
