from abc import ABC, abstractmethod
from typing import Dict

from playwright.sync_api import BrowserContext, Page

from crawlers.Types import ArticleReturnType


class Spider(ABC):
    def __init__(self, context: BrowserContext, page: Page, options: object) -> None:
        super().__init__()
        self.context = context
        self.page = page
        self.options = options

    @abstractmethod
    def run(self, url: str) -> ArticleReturnType:
        pass
