from . import ContestInfo
from boltons import strutils


def create_folder_name(contest_info: ContestInfo) -> str:
    return strutils.slugify(contest_info.short_name)
