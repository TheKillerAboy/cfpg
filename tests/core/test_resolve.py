import pytest
from cfpg.core import resolve


@pytest.mark.integration
def test_get_contest_history_for_page():
    contest_info, last_page = resolve.get_contest_history_for_page(1)

    assert last_page > 1
    assert len(contest_info) > 0
