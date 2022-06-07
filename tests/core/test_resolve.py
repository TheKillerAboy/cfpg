from unittest.mock import patch
import pytest
from cfpg.core import resolve

##################################################################
# helper
##################################################################


@pytest.fixture
def get_content_history_mock(contest_history):
    with patch("cfpg.core.resolve.api_call", return_value=contest_history):
        yield


##################################################################
# get_contest_history
##################################################################


@pytest.mark.integration
def test_get_content_history():
    contest_history = resolve.get_content_history()

    assert len(contest_history) > 0


##################################################################
# resolve_contest
##################################################################


@pytest.mark.parametrize(
    "contest_str,contest_id,short_name",
    [
        ("1696", 1696, "1696"),
        ("1681", 1681, "ECF-129-DIV-2"),
        ("CF-799", 1692, "CF-799-DIV-4"),
        ("CF-799-DIV-4", 1692, "CF-799-DIV-4"),
        ("CF-800-DIV-2", 1694, "CF-800-DIV-2"),
        ("CF-800-DIV-1", 1693, "CF-800-DIV-1"),
        ("CF-800-1", 1693, "CF-800-DIV-1"),
        ("ECF-129", 1681, "ECF-129-DIV-2"),
    ],
)
def test_resolve_contest(contest_str, contest_id, short_name, get_content_history_mock):
    contest_info = resolve.resolve_contest(contest_str)
    assert contest_info.id == contest_id
    assert contest_info.short_name == short_name


@pytest.mark.parametrize(
    "contest_str,exception",
    [
        ("CF-800", resolve.MultiContestStrResolveDivError),
        ("CF-999999", resolve.ContestStrResolveError),
        ("SOMETHING-999999", resolve.ContestStrResolveError),
    ],
)
def test_resolve_contest_except(contest_str, exception, get_content_history_mock):
    with pytest.raises(exception):
        resolve.resolve_contest(contest_str)
