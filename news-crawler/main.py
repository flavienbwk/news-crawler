# -*- coding: utf-8 -*-

import os
import time

import slugify
from playwright.sync_api import sync_playwright

from crawlers import CRAWLERS
from crawlers.Crawler import Crawler
from crawlers.Login import Login
from models.Media import Media
from utils import Database, Logger, Persister

FILE_PATH = os.path.realpath(__file__)
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
COOKIES_DIR = f"{DIR_PATH}/../database"

PERSIST_BATCH = 1  # Number of articles to be saved at the same time
PAGE_HEIGHT = 850
PAGE_WIDTH = 768

CRAWLER_EMAIL = os.getenv("CRAWLER_EMAIL")
CRAWLER_PASSWORD = os.getenv("CRAWLER_PASSWORD")

LOGGER = Logger.Logger()
LOGGER.info("Starting News Crawler...")


CRAWLER_OPTIONS = {
    "page_height": PAGE_HEIGHT,
    "page_width": PAGE_WIDTH,
    "retrieve_related_article_links": (
        True
        if os.environ.get("RETRIEVE_RELATED_ARTICLE_LINKS", False) == "true"
        else False  # May lead to irrelevant articles throughout time (liens "Lire aussi...")
    ),
    "retrieve_each_article_links": (
        True
        if os.environ.get("RETRIEVE_EACH_ARTICLE_LINKS", False) == "true"
        else False  # May highly lead to irrelevant articles throughout time
    ),
}


def get_media(database: Database, sha256: str) -> Media:
    session = database.getSession()
    return session.query(Media).filter_by(sha256=sha256).first()


def process_crawl(crawler_source: str, database: Database.Database):
    login_class: Login = CRAWLERS[crawler_source]["login"]
    crawler_class: Crawler = CRAWLERS[crawler_source]["crawler"]
    persister = Persister.Persister(database=database, batch_size=PERSIST_BATCH)

    with sync_playwright() as playwright_rs:
        is_docker = True if os.environ.get("IS_DOCKER", False) == "true" else False
        browser = playwright_rs.chromium.launch(headless=True if is_docker else False)
        context = browser.new_context()
        page = context.new_page()
        page.set_default_timeout(60000)
        page.set_viewport_size({"width": PAGE_WIDTH, "height": PAGE_HEIGHT})

        cookies_file_path = (
            f"{COOKIES_DIR}/{slugify.slugify(crawler_source)}.cookies.pickle"
        )
        login = login_class(
            cookies_file_path=cookies_file_path,
            context=context,
            page=page,
            crawler_email=CRAWLER_EMAIL,
            crawler_password=CRAWLER_PASSWORD,
        )
        login.login()

        crawler = crawler_class(
            database=database, context=context, page=page, options=CRAWLER_OPTIONS
        )

        for article_details in crawler.crawl():
            if article_details:
                article = article_details["article"]
                for media in article_details["medias"]:
                    if media:
                        media_query = get_media(database, media.sha256)
                        if media_query:
                            media = media_query
                        article.medias.append(media)
                persister.add_object(article)
                persister.request_save_objects()
        persister.save_objects()


if __name__ == "__main__":

    start_time = time.time()
    CRAWLER_SOURCE = os.environ.get("CRAWLER_SOURCE", "")
    if CRAWLER_SOURCE not in CRAWLERS:
        LOGGER.error(f"Provided crawler '{CRAWLER_SOURCE}' is not supported")
        exit(1)

    database = Database.Database("sqlite")
    database.initDatabase()

    process_crawl(CRAWLER_SOURCE, database)
    print("--- Executed in %s seconds ---" % (time.time() - start_time))
