# Manages login strategy
import os
import random
import time
import traceback

import playwright
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
        is_login_needed = True
        if self.load_cookies():
            self.page.goto(os.environ.get("START_LINK", "https://www.lemonde.fr/"))
            try:
                self.page.wait_for_load_state()
                badge_subscribed = self.page.query_selector(
                    "div.Connexion__account > a > span.AccountMenu > span.AccountMenu__type > span"
                )
                is_login_needed = True if badge_subscribed == None else False
            except playwright._impl._api_types.TimeoutError as e:
                print(traceback.format_exc())
                LOGGER.warning("Need to login again !")

        if is_login_needed:
            LOGGER.info("Logging in...")
            self.page.goto("https://secure.lemonde.fr/sfuser/connexion")

            # Skip GPDR modal
            time.sleep(2)
            gpdr_selector = "body > div.gdpr-lmd-standard.gdpr-lmd-standard--transparent-deny > div > header > a"
            try:
                self.page.wait_for_selector(gpdr_selector)
                self.page.click(gpdr_selector)
            except playwright._impl._api_types.TimeoutError as e:
                LOGGER.info("No GPDR modal found. Trying to login...")

            # Login
            self.page.wait_for_selector("#email")
            self.page.type("#email", self.crawler_email, delay=random.randint(30, 120))
            self.page.wait_for_selector("#password")
            self.page.type(
                "#password", self.crawler_password, delay=random.randint(30, 120)
            )
            self.page.wait_for_selector("#login > main > form > div > .button")
            self.page.click("#login > main > form > div > .button")
            LOGGER.info("Logged in !")
            time.sleep(4)

            self.save_cookies()
            self.page.goto(os.environ.get("START_LINK", "https://www.lemonde.fr/"))
        else:
            LOGGER.info("Good, we're connected back.")
