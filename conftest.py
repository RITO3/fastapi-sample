from datetime import datetime
from typing import List
from py.xml import Tag, html
import pytest


def pytest_html_results_table_header(cells: List[Tag]):
    cells.insert(1, html.th("Test Case"))
    cells.insert(2, html.th("Time", class_="sortable time", col="time"))
    cells.pop()


def pytest_html_results_table_row(report, cells: List[Tag]) -> None:
    cells.insert(1, html.td(report.description))
    cells.insert(2, html.td(str(datetime.now()), class_="col-time"))
    cells.pop()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)
