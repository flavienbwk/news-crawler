from abc import ABC, abstractmethod
from typing import Dict, Iterable, List

from playwright.sync_api import BrowserContext, Page
from utils.Database import Database

from crawlers.Types import ArticleReturnType


class Crawler(ABC):
    def __init__(
        self,
        database: Database,
        context: BrowserContext,
        page: Page,
        options: object,
    ) -> None:
        super().__init__()
        self.database = database
        self.context = context
        self.page = page
        self.options = options

    @abstractmethod
    def crawl(self) -> Iterable[ArticleReturnType]:
        pass
