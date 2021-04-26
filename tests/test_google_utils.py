import pytest
from utils import google_utils
from datetime import datetime
import gspread


def test_get_formatted_time():
    """Ensure we keep the proper time formatting"""
    assert datetime.strftime(datetime.now(), '%B %d, %Y %H:%M:%S') == google_utils.get_formatted_time()


@pytest.mark.parametrize("time,correct",
                         [(1589339028, '2020-05-13 03:03:48'),
                          (1001, '1970-01-01 00:16:41'),
                          (2000000, '1970-01-24 03:33:20'),
                          (2e10, '2603-10-11 11:33:20')])
def test_convert_reddit_timestamp(time, correct):
    """Test that we can convert properly from unix time to human-readable format."""
    assert google_utils.convert_reddit_timestamp(time) == correct


def test_create_gspread_client():
    """Test that we can create a gspread client"""
    assert isinstance(google_utils.create_gspread_client(), gspread.Client)


# TODO
def test_update_df():
    """Test that we properly concatenate to the df"""
    assert True == True


def test_get_current_tab_name():
    """Assert that the current Tab Name is <Month> <Year>"""
    assert datetime.strftime(datetime.now(), '%B %Y') == google_utils.get_current_tab_name()


class Sheet:
    """Mock for a gspread Spreadsheet for testing test_get_specific_tab_url"""
    def __init__(self, url):
        self.url = url

    def worksheet(self, tab_name):
        class Tab:
            def __init__(self, id):
                self.id = id
        return Tab(tab_name)


@pytest.mark.parametrize("url,id",
                         [("abc", "123"),
                          ("doremi", "easy")])
def test_get_specific_tab_url(url, id):
    assert url + '/edit#gid=' + id == google_utils.get_specific_tab_url(Sheet(url), id)
