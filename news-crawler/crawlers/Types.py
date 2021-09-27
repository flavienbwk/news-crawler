from typing import NamedTuple, List

from models.Article import Article
from models.Media import Media


class ArticleReturnType(NamedTuple):
    article: Article
    medias: List[Media]
