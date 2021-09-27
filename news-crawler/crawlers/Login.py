# Manages login strategy
import os
import pickle
from abc import ABC, abstractmethod

from playwright.sync_api import BrowserContext, Page


class Login(ABC):
    def __init__(
        self,
        cookies_file_path: str,
        context: BrowserContext,
        page: Page,
        crawler_email: str = "",
        crawler_password: str = "",
    ) -> None:
        super().__init__()
        self.context = context
        self.page = page
        self.crawler_email = crawler_email
        self.crawler_password = crawler_password
        self.cookies_file_path = cookies_file_path

    @abstractmethod
    def login(self) -> None:
        pass

    def load_cookies(self) -> bool:
        """Loads cookies to browser from cookies file.

        Returns:
            bool: Were cookies successfuly loaded ?
        """
        if not self.cookies_file_path:
            return True
        if os.path.exists(self.cookies_file_path):
            with open(self.cookies_file_path, "rb") as cookies_fs:
                cookies = pickle.loads(cookies_fs.read())
            self.context.add_cookies(cookies)
            return True
        return False

    def save_cookies(self) -> None:
        if not self.cookies_file_path:
            return
        cookies = self.context.cookies()
        with open(self.cookies_file_path, "wb+") as cookies_fs:
            cookies_fs.write(pickle.dumps(cookies))
