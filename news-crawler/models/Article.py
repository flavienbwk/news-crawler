from sqlalchemy import Column, DateTime, String, Text, func
from sqlalchemy.orm import relationship

from models.Article_has_Media import Article_has_Media
from models.base import base


class Article(base):
    __tablename__ = "Article"

    url = Column(String, primary_key=True)
    source = Column(String, unique=False, nullable=False)
    title = Column(String, unique=False, nullable=True)
    author = Column(String, unique=False, nullable=True)
    headline = Column(Text, unique=False, nullable=True)
    article = Column(Text, unique=False, nullable=True)
    language = Column(String(3), unique=False, nullable=True)  # 3-letter ISO code
    published_at_txt = Column(String, nullable=True)
    published_at = Column(DateTime, nullable=True)
    added_at = Column(DateTime, server_default=func.now())
    medias = relationship(
        "Media", secondary=Article_has_Media, back_populates="articles"
    )

    def __repr__(self):
        return f"<Article(url='{self.url}', source='{self.source}', title='{self.title}', headline='{self.headline}', added_at='{self.added_at}')>"
