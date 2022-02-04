try:
    from src.scripts.build_site import delete_output_file_space
except ImportError:
    # Some people have issues with the above import. Try this one as well, just to see if it works.
    from build_site import delete_output_file_space
from utils import find_project_root

find_project_root()
delete_output_file_space()
