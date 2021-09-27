import time
from typing import Dict

from crawlers.Spider import Spider as SpiderBase
from crawlers.Types import ArticleReturnType
from models.Article import Article
from models.Media import Media
from playwright.sync_api import BrowserContext, Page
from utils import Logger
from utils.crawl import (
    cleanhtml,
    get_html_from_one_of_selectors,
    get_html_from_selector,
    random_activity,
)
from utils.hash import sha256_bytes

LOGGER = Logger.Logger()


class Spider(SpiderBase):
    def __init__(
        self,
        context: BrowserContext,
        page: Page,
        options: object,
    ) -> None:
        super().__init__(context, page, options)

    def run(self, url: str) -> ArticleReturnType:
        self.page.goto(url)
        random_activity(
            self.page, self.options["page_height"], self.options["page_width"]
        )
        time.sleep(1)
        random_activity(
            self.page, self.options["page_height"], self.options["page_width"]
        )

        article_content_html = ""
        article_contents = self.page.query_selector_all(".article__paragraph")
        for article_content in article_contents:
            article_content_html += "\n\n" + article_content.inner_html()

        try:
            article_image = self.page.query_selector(
                "section.article__wrapper > article > figure > img"
            )
            article_image_bytes = article_image.screenshot()
        except AttributeError:
            LOGGER.info("No image found for this article")
            article_image_bytes = None

        article_title_html = get_html_from_selector(self.page, "h1.article__title")
        article_headline_html = get_html_from_selector(self.page, ".article__desc")
        article_date_html = get_html_from_selector(self.page, ".meta__date")
        article_author_html = get_html_from_one_of_selectors(
            self.page,
            [
                "#js-authors-list",
                ".article__author-link",
                ".article__author-description",
                ".meta__author",
            ],
        )

        illustration = (
            Media(
                sha256=sha256_bytes(article_image_bytes),
                blob=article_image_bytes,
            )
            if article_image_bytes
            else None
        )

        article = Article(
            source="Le Monde",
            language="fra",
            url=url,
            title=cleanhtml(article_title_html),
            headline=cleanhtml(article_headline_html),
            article=cleanhtml(article_content_html),
            author=cleanhtml(article_author_html),
            published_at_txt=cleanhtml(article_date_html),
        )
        return {"article": article, "medias": [illustration]}
