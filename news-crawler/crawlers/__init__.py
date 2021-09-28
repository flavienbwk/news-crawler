from .lemonde.Crawler import Crawler as LeMondeCrawler
from .lemonde.Login import Login as LeMondeLogin

from .reuters.Crawler import Crawler as ReutersCrawler
from .reuters.Login import Login as ReutersLogin

CRAWLERS = {
    "lemonde": {
        "crawler": LeMondeCrawler,
        "login": LeMondeLogin,
    },
    "reuters": {
        "crawler": ReutersCrawler,
        "login": ReutersLogin,
    },
}
