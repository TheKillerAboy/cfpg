from concurrent.futures import Future, ThreadPoolExecutor
from functools import lru_cache
import re
from textwrap import indent
from threading import Lock
from typing import Dict, List, Tuple
from bs4 import BeautifulSoup, Tag

import requests


def get_contest_history_for_page(page_id: int) -> Tuple[Dict[str, int], int]:
    out = {}

    res = requests.get(f"https://codeforces.com/contests/page/{page_id}?complete=true")

    soup = BeautifulSoup(res.content, "html.parser")

    contests_table_div = soup.find("div.contests-table")

    print(soup)

    for contest_tr in contests_table_div.find_all("tr"):
        if contest_tr.has_attr("data-contestid"):
            name_td: Tag = contest_tr.find("td")
            display_name = name_td.text
            id_ext = name_td.find("a")["href"]

            id = int(re.match("/contest/(\d+)", id_ext).group(1))

            out[display_name] = id

    # gather max page
    pagination_div = soup.find("div.pagination")
    last_page_li = pagination_div.find_all("li")[-1]
    last_page = int(last_page_li.find("span")["pageindex"])

    return out, last_page


@lru_cache
def get_content_history() -> Dict[str, int]:
    lock = Lock()
    max_page = 50

    def wrapper(page_id: int) -> Dict[str, int]:
        with lock:
            if page_id > max_page:
                return {}

        out, last_page = get_contest_history_for_page(page_id)

        with lock:
            max_page = last_page

        return out

    futures: List[Future] = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        # max_workers should be more than current max pages
        for page_id in range(max_page):
            futures.append(executor.submit(wrapper, page_id))

    out = {}

    for future in futures:
        out.update(future.result())

    return out


def resolve_from_contest_history(re_str, flags=None):
    contest_history = get_content_history()

    re_comp = re.compile(re_str, flags=flags)

    results = []

    for display_name, contest_id in contest_history.items():
        if match := re_comp.match(display_name):
            results.append(match, contest_id)

    return match


class MultiContestStrResolveDivError(Exception):
    def __init__(self, display_names):
        self.display_names = display_names
        super().__init__(
            "Unable to resolve contest string, unkown division:\n"
            + indent("\n".join(display_names), "- ")
        )


class ContestStrResolveError(Exception):
    def __init__(self, contest_str):
        self.contest_str = contest_str
        super().__init__(f"Unable to resolve contest string: `{contest_str}`")


def resolve_with_div(contest_str, re_str, div=None, flags=None):
    results = resolve_from_contest_history(re_str, flags=flags)

    if len(results) == 0:
        raise ContestStrResolveError(contest_str)

    if len(results) > 1:
        raise MultiContestStrResolveDivError([match.group(0) for match, _ in results])

    return results[0][1]


def resolve_cf(cf, div=None):
    div = r"\d+" if div is None else div
    return resolve_with_div(
        cf,
        rf"Codeforces Round #(?P<contest_id>{cf}) \(.*Div. (?P<contest_div>{div}.*)\)",
        div=div,
    )


def resolve_ecf(ecf, div=None):
    div = r"\d+" if div is None else div
    return resolve_with_div(
        ecf,
        rf"Educational Codeforces Round (?P<contest_id>{ecf}) \(.*Div. (?P<contest_div>{div}.*)\)",
        div=div,
    )


def resolve_contest(contest_str: str) -> int:
    if contest_match := re.match(r"\d+", contest_str):
        return int(contest_match.group(0))

    if contest_match := re.match(r"CF-(\d+)(-DIV-(\d+))?", contest_str, re.IGNORECASE):
        return resolve_cf(contest_match.group(1), contest_match.group(3))

    if contest_match := re.match(r"ECF-(\d+)(-DIV-(\d+))?", contest_str, re.IGNORECASE):
        return resolve_ecf(contest_match.group(1), contest_match.group(3))

    raise ContestStrResolveError(contest_str)
