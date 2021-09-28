import random
import time

from crawlers.Spider import Spider as SpiderBase
from crawlers.Types import ArticleReturnType
from models.Article import Article
from models.Media import Media
from playwright.sync_api import BrowserContext, Page
from utils import Logger
from utils.crawl import (
    cleanhtml,
    get_elements_from_selector,
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

        # Skip GPDR modal
        self.page.wait_for_selector("button.ot-pc-refuse-all-handler")
        self.page.query_selector("button.ot-pc-refuse-all-handler").click()

        random_activity(self.page, intensifier=2.5)
        time.sleep(random.randint(0, 2))
        random_activity(self.page, intensifier=2.5)

        article_content_html = ""
        article_contents = self.page.query_selector_all(
            "div[class^='ArticleBody__content'] p"
        )
        for article_content in article_contents:
            article_content_html += "\n\n" + article_content.inner_html()

        medias = []
        article_image_bytes = None
        try:
            article_images = get_elements_from_selector(
                self.page, "div[class^='ArticleBody__container'] img"
            )
            if article_images:
                for article_image in article_images:
                    article_image_bytes = article_image.screenshot()
                    if article_image_bytes:
                        medias.append(
                            Media(
                                sha256=sha256_bytes(article_image_bytes),
                                blob=article_image_bytes,
                            )
                        )
        except AttributeError:
            LOGGER.debug("No image found for this article")

        article_title_html = get_html_from_selector(
            self.page, "div[class^='Article__container'] h1[class^='Text__text']"
        )
        article_headline_html = ""
        article_date_html = get_html_from_selector(
            self.page, "div[class^='Article__container'] time[class^='Text__text']"
        )
        article_author_html = get_html_from_one_of_selectors(
            self.page,
            [
                "div[class*='ArticleHeader__author']",
            ],
        )

        article = Article(
            source="Reuters",
            language="eng",
            url=url,
            title=cleanhtml(article_title_html),
            headline=cleanhtml(article_headline_html),
            article=cleanhtml(article_content_html),
            author=cleanhtml(article_author_html),
            published_at_txt=cleanhtml(article_date_html),
        )

        return {"article": article, "medias": medias}
