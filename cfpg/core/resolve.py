from dataclasses import dataclass
import re
from textwrap import indent
from typing import List
from . import api_call
from datetime import datetime, timedelta


@dataclass
class ContestInfo:
    id: int
    name: str
    type: str
    phase: str
    frozen: bool
    durationSeconds: timedelta
    startTimeSeconds: datetime
    relativeTimeSeconds: timedelta
    short_name: str

    @classmethod
    def build(cls, raw):
        raw["durationSeconds"] = timedelta(seconds=raw["durationSeconds"])
        raw["startTimeSeconds"] = datetime.fromtimestamp(raw["startTimeSeconds"])
        raw["relativeTimeSeconds"] = timedelta(seconds=raw["relativeTimeSeconds"])
        if "short_name" not in raw:
            raw["short_name"] = str(raw["id"])

        return ContestInfo(**raw)


def get_content_history() -> List[ContestInfo]:
    data = api_call("contest.list", params={"gym": False})

    return [ContestInfo.build(contest) for contest in data]


def resolve_from_contest_history(re_str, flags=0):
    contest_history = get_content_history()

    re_comp = re.compile(re_str, flags=flags)

    results = []

    for contest_info in contest_history:
        if match := re_comp.match(contest_info.name):
            results.append((match, contest_info))

    return results


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


def resolve_with_div(contest_str, re_str, short_format, flags=0):
    results = resolve_from_contest_history(re_str, flags=flags)

    if len(results) == 0:
        raise ContestStrResolveError(contest_str)

    if len(results) > 1:
        raise MultiContestStrResolveDivError([match.group(0) for match, _ in results])

    match = results[0][0]
    contest_info = results[0][1]
    contest_info.short_name = short_format.format(**match.groupdict())

    return contest_info


def resolve_cf(cf, div=None) -> ContestInfo:
    div = r"\d+" if div is None else div
    return resolve_with_div(
        cf,
        rf"Codeforces Round #(?P<contest_id>{cf}) \(.*Div. (?P<contest_div>{div}).*\)",
        "CF-{contest_id}-DIV-{contest_div}",
    )


def resolve_ecf(ecf, div=None) -> ContestInfo:
    div = r"\d+" if div is None else div
    return resolve_with_div(
        ecf,
        rf"Educational Codeforces Round (?P<contest_id>{ecf}) \(.*Div. (?P<contest_div>{div}).*\)",
        "ECF-{contest_id}-DIV-{contest_div}",
    )


def resolve_id(contest_id: int) -> ContestInfo:
    contest_history = get_content_history()

    for contest_info in contest_history:
        if contest_info.id == contest_id:
            return contest_info

    raise ContestStrResolveError(str(contest_id))


def resolve_contest(contest_str: str) -> ContestInfo:
    if contest_match := re.match(r"\d+", contest_str):
        return resolve_id(int(contest_match.group(0)))

    if contest_match := re.match(r"CF-(\d+)(-DIV-(\d+))?", contest_str, re.IGNORECASE):
        return resolve_cf(contest_match.group(1), contest_match.group(3))

    if contest_match := re.match(r"ECF-(\d+)(-DIV-(\d+))?", contest_str, re.IGNORECASE):
        return resolve_ecf(contest_match.group(1), contest_match.group(3))

    raise ContestStrResolveError(contest_str)
