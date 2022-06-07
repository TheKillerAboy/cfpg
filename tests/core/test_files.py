import pytest

from cfpg.core import files

##################################################################
# create_folder_name
##################################################################


@pytest.mark.parametrize(
    "contest_info,filename",
    [
        (pytest.lazy_fixture("contest_history_1681"), "ecf_129_div_2"),
        (pytest.lazy_fixture("contest_history_1696"), "1696"),
    ],
)
def test_create_folder_name(contest_info, filename):
    assert files.create_folder_name(contest_info) == filename
