import re
import traceback
from typing import Iterable, List, Union
from urllib.parse import urljoin, urlparse

import tqdm
from crawlers.Crawler import Crawler as CrawlerBase
from crawlers.lemonde.Spider import Spider
from crawlers.Types import ArticleReturnType
from models.Article import Article
from playwright.sync_api import BrowserContext, ElementHandle, Page
from utils import Logger
from utils.Database import Database

LOGGER = Logger.Logger()


def was_article_crawled(database: Database, url: str) -> bool:
    session = database.getSession()
    return True if session.query(Article).filter_by(url=url).count() else False


def get_article_links_from_element(element: Union[Page, ElementHandle]) -> List[str]:
    hrefs_of_page = element.eval_on_selector_all(
        "a[href^='https://www.lemonde.fr/']",
        "elements => elements.map(element => element.href)",
    )

    # Filtering only article links
    article_hrefs = []
    for href in hrefs_of_page:
        if re.match("https:\/\/www\.lemonde\.fr\/.*\/article\/.*", href):
            href = urljoin(href, urlparse(href).path)
            if href not in article_hrefs:
                article_hrefs.append(href)
    return article_hrefs


class Crawler(CrawlerBase):
    def __init__(
        self,
        database: Database,
        context: BrowserContext,
        page: Page,
        options: object,
    ) -> None:
        super().__init__(database, context, page, options)

    def crawl(self) -> Iterable[ArticleReturnType]:
        self.page.wait_for_load_state()
        article_hrefs = get_article_links_from_element(self.page)
        not_working_hrefs = []
        nb_total_articles = len(article_hrefs)

        with tqdm.tqdm(
            total=nb_total_articles, position=0, leave=True, unit="article"
        ) as pbar:
            while article_hrefs:
                pbar.update(1)
                article_href = article_hrefs.pop()

                LOGGER.debug(f"Processing {article_href}...")
                if was_article_crawled(self.database, article_href):
                    LOGGER.debug(f"Article already in database : {article_href}")
                    pbar.update(0)
                    continue

                try:
                    spider = Spider(self.context, self.page, self.options)
                    article_details = spider.run(article_href)
                    yield article_details

                    new_urls = self.get_page_links(article_hrefs, not_working_hrefs)
                    for new_url in new_urls:
                        article_hrefs.append(new_url)
                    nb_total_articles += len(new_urls)
                except Exception as e:
                    not_working_hrefs.append(article_href)
                    LOGGER.info(traceback.format_exc())
                    LOGGER.info(e)
                    yield None

                pbar.total = nb_total_articles
                pbar.refresh()

    def get_page_links(
        self, current_article_hrefs: List[str], not_working_hrefs: List[str]
    ):
        new_hrefs = []
        try:
            if self.options["retrieve_related_article_links"]:
                new_article_links = get_article_links_from_element(
                    self.page.query_selector(".article__wrapper")
                )
                for new_article_link in new_article_links:
                    if (
                        was_article_crawled(self.database, new_article_link) is False
                        and new_article_link not in not_working_hrefs
                        and new_article_link not in current_article_hrefs
                    ):
                        new_hrefs.append(new_article_link)
        except AttributeError as e:
            LOGGER.info("Could not retrieve more links for this article", flush=True)

        if self.options["retrieve_each_article_links"]:
            new_article_links = get_article_links_from_element(self.page)
            for new_article_link in new_article_links:
                if (
                    was_article_crawled(self.database, new_article_link) is False
                    and new_article_link not in not_working_hrefs
                    and new_article_link not in current_article_hrefs
                ):
                    new_hrefs.append(new_article_link)
        return new_hrefs
