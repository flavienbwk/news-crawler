from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, func

from models.base import base

Article_has_Media = Table(
    "Article_has_Media",
    base.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("article_url", String, ForeignKey("Article.url")),
    Column("media_sha256", Integer, ForeignKey("Media.sha256")),
    Column("added_at", DateTime, server_default=func.now()),
)
