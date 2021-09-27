import random
import time
from typing import List, Union

import lxml.html
import lxml.html.clean
from playwright.sync_api import Page, ElementHandle

from utils import Logger

LOGGER = Logger.Logger()


def cleanhtml(raw_html: str) -> str:
    """Removes all tags from HTML string keeping only inner texts"""
    if raw_html:
        try:
            doc = lxml.html.fromstring(raw_html)
            cleaner = lxml.html.clean.Cleaner(style=True)
            doc = cleaner.clean_html(doc)
            return doc.text_content().strip()
        except lxml.etree.ParserError:
            pass
    return ""


def get_html_from_selector(page: Page, selector: str) -> str:
    """Returns the inner HTML of an element on the page from
    its provided selector, or an empty string"""
    try:
        item = page.query_selector(selector)
        return item.inner_html()
    except Exception as e:
        LOGGER.debug(f"Can't get selector {selector}")
        return ""


def get_html_from_one_of_selectors(page: Page, selectors: List[str]) -> str:
    """Returns the inner HTML of an element on the page from
    one of its provided selectors, or an empty string.
    First element found in returned.
    """
    item_html = ""
    for selector in selectors:
        if len(item_html) == 0:
            item_html_query = get_html_from_selector(page, selector)
            item_html = item_html_query if item_html_query else ""
        if item_html:
            break
    return item_html


def get_element_from_selector(page: Page, selector: str) -> Union[ElementHandle, None]:
    """Returns the element on the page from
    its provided selector, or None"""
    try:
        return page.query_selector(selector)
    except Exception as e:
        LOGGER.info(f"Can't get selector {selector}")
        return None


def get_element_from_one_of_selectors(
    page: Page, selectors: List[str]
) -> Union[ElementHandle, None]:
    """Returns the element on the page from
    one of its provided selectors, or None.
    First element found in returned.
    """
    item = None
    for selector in selectors:
        item = get_element_from_selector(page, selector)
        if item:
            break
    return item


def get_elements_from_selector(page: Page, selector: str) -> Union[ElementHandle, None]:
    """Returns the elements on the page from
    their provided selector, or None"""
    try:
        return page.query_selector_all(selector)
    except Exception as e:
        LOGGER.info(f"Can't get selector {selector}")
        return None


def get_elements_from_one_of_selectors(
    page: Page, selectors: List[str]
) -> Union[ElementHandle, None]:
    """Returns the elements on the page from
    one of their provided selectors, or None.
    First element found in returned.
    """
    item = None
    for selector in selectors:
        item = get_elements_from_selector(page, selector)
        if item is not None:
            break
    return item


def random_scroll(page: Page):
    size = page.viewport_size
    scroll_to = int(size["height"] * (1.0 - (random.randrange(1, 8) / 10)))
    page.evaluate(f"window.scrollBy(0, {scroll_to})")


def random_mouse_move(page: Page, max_height: int, max_width: int):
    y = random.randint(0, max_height)
    x = random.randint(0, max_width)
    page.mouse.move(x, y)


def random_activity(page: Page, page_height: int, page_width: int):
    """Simulates user activity on page"""
    random_scroll(page)
    time.sleep(random.randint(0, 1000) / 1000.0)
    random_mouse_move(page, page_height, page_width)
    time.sleep(random.randint(0, 1000) / 1000.0)
    random_mouse_move(page, page_height, page_width)
    time.sleep(random.randint(0, 1000) / 1000.0)
    random_mouse_move(page, page_height, page_width)
    time.sleep(random.randint(0, 1000) / 1000.0)
