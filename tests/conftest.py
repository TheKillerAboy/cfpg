import json
import pytest

from cfpg.core.resolve import ContestInfo

##################################################################
# fixtures
##################################################################


##################################################################
# contest_history
##################################################################


@pytest.fixture()
def contest_history():
    with open("tests/fixtures/contest_history.json", "r") as f:
        return json.load(f)


@pytest.fixture()
def contest_history_info(contest_history):
    return [ContestInfo.build(contest) for contest in contest_history]


@pytest.fixture()
def contest_history_info_mapped(contest_history_info):
    return {contest_info.id: contest_info for contest_info in contest_history_info}


@pytest.fixture()
def contest_history_1681(contest_history_info_mapped):
    return contest_history_info_mapped[1681]


@pytest.fixture()
def contest_history_1696(contest_history_info_mapped):
    return contest_history_info_mapped[1696]


@pytest.fixture()
def contest_history_1695(contest_history_info_mapped):
    return contest_history_info_mapped[1695]


@pytest.fixture()
def contest_history_1693(contest_history_info_mapped):
    return contest_history_info_mapped[1693]


@pytest.fixture()
def contest_history_1694(contest_history_info_mapped):
    return contest_history_info_mapped[1694]


@pytest.fixture()
def contest_history_1692(contest_history_info_mapped):
    return contest_history_info_mapped[1692]


@pytest.fixture()
def contest_history_1697(contest_history_info_mapped):
    return contest_history_info_mapped[1697]


@pytest.fixture()
def contest_history_1689(contest_history_info_mapped):
    return contest_history_info_mapped[1689]
