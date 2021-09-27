from .lemonde.Crawler import Crawler as LeMondeCrawler
from .lemonde.Login import Login as LeMondeLogin

CRAWLERS = {
    "lemonde": {
        "crawler": LeMondeCrawler,
        "login": LeMondeLogin,
    }
}
