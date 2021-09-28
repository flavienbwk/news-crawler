# :spider: News crawler

Playwright-powered modulable news crawler.

If you need web security consulting to avoid scraping, contact me on [berwick.fr](https://berwick.fr/en) !

---

| Supported newspaper | CRAWLER_SOURCE | Requires account            |
| ------------------- | -------------- | --------------------------- |
| Le Monde            | `lemonde`      | Yes _(Premium recommended)_ |
| Reuters             | `reuters`      | No                          |

:warning: **DISCLAIMER : This project is for educational purpose only ! Do NOT use it for any other intent.** It was developed as a fun side-project to train my scraping skills.

## Extraction

News-Crawler browses articles from newspaper websites and store them in a SQLite database :

- Source
- URL
- Title
- Headline
- Article
- Author
- Image**s**
- Publication date
- Language

## Getting started

### Docker

1. Copy and fill your credentials in `.env` :

    ```bash
    git clone https://github.com/flavienbwk/news-crawler && cd news-crawler
    cp .env.example .env
    ```

    Edit `CRAWLER_SOURCE`, `CRAWLER_EMAIL` and `CRAWLER_PASSWORD` matching your newspaper credentials

2. Run container

    ```bash
    docker-compose run crawler
    ```

### CLI

> Requires Python >= 3.7 and pip installed

1. Install dependencies

    ```bash
    git clone https://github.com/flavienbwk/news-crawler && cd news-crawler
    pip3 install -r requirements.txt
    ```

2. Run CLI

    ```bash
    CRAWLER_SOURCE='...' CRAWLER_EMAIL='...' CRAWLER_PASSWORD='...' python3 ./scripts/crawler.py
    ```

### Parameters

| Name                           | Type | Description                                                                 |
| ------------------------------ | ---- | --------------------------------------------------------------------------- |
| CRAWLER_SOURCE                 | str  | Slug corresponding to the crawler to use (e.g: `lemonde`, `reuters`)        |
| CRAWLER_EMAIL                  | str  | Newspaper email address                                                     |
| CRAWLER_PASSWORD               | str  | Newspaper password                                                          |
| START_LINK                     | str  | After login, start scraping articles from this page                         |
| RETRIEVE_RELATED_ARTICLE_LINKS | bool | Crawl links in currently scraped article pointing to other similar articles |
| RETRIEVE_EACH_ARTICLE_LINKS    | bool | Crawl all article links present in the currently scraped article            |

## Development

### Working principle flow

1. Init : Playwright and flow initialization (browser context, logging)
2. Logins : manage login strategy to website with periodic login check capabilities
3. Crawlers : manage crawling strategy and yield {`models.Article` and `models.Media` objects}
4. Spiders : retrieve data from webpage
5. Persister : manage database persistance strategy

### Creating a new crawler

We recommend you to copy `./news-crawler/crawlers/lemonde` to `./news-crawler/crawlers/yourcrawler`. Now edit :

- `Login.py`
- `Crawler.py`
- `Spider.py`

Don't forget to add a reference to your crawler in [`./news-crawler/crawlers/__init__.py`](./news-crawler/crawlers/__init__.py)

### Architecture

```txt
.
├── database                # Directory where article database and login cookies are saved
├── docker-compose.yml
├── Dockerfile
├── logs                    # Directory where logs are saved
├── news-crawler            # Source directory
│   ├── crawlers
│   │   ├── Crawler.py      # Abstract class containing helper functions to re-implement a crawler
│   │   ├── __init__.py     # Links CRAWLER_SOURCE to a crawling flow
│   │   ├── lemonde         # Implementation of a News Crawler flow for Le Monde
│   │   │   ├── Crawler.py  # Manages crawling strategy (which links to visit)
│   │   │   ├── Login.py    # Manages login to website strategy
│   │   │   └── Spider.py   # Scraps article data from provided link
│   │   ├── Login.py        # Abstract class containing helper functions to re-implement a login strategy
│   │   ├── Spider.py       # Abstract class containing helper functions to re-implement a scraping strategy
│   │   └── Types.py        # Nice typing variables
│   ├── main.py             # Main script to run News Scraper flow
│   ├── models              # Database models
│   └── utils               # Helper functions and classes inside
│       ├── crawl.py        # Crawl helper functions
│       ├── Database.py     # Database management class
│       ├── hash.py         # Hash-related helper functions
│       ├── Logger.py       # Logging class
│       └── Persister.py    # Class to manage persistance strategy
├── README.md
└── requirements.txt        # Python requirements strategy
```
