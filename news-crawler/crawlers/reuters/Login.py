# Manages login strategy
from playwright.sync_api import BrowserContext, Page

from utils import Logger
from crawlers.Login import Login as LoginBase

LOGGER = Logger.Logger()


class Login(LoginBase):
    def __init__(
        self,
        cookies_file_path: str,
        context: BrowserContext,
        page: Page,
        crawler_email: str = "",
        crawler_password: str = "",
    ) -> None:
        super().__init__(
            cookies_file_path, context, page, crawler_email, crawler_password
        )

    def login(self) -> None:
        LOGGER.info("No need to login.")
