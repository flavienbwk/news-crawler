from sqlalchemy import LargeBinary, Column, DateTime, String, func
from sqlalchemy.orm import relationship

from models.Article_has_Media import Article_has_Media
from models.base import base


class Media(base):
    __tablename__ = "Media"

    sha256 = Column(String(64), primary_key=True)
    blob = Column(LargeBinary, unique=False, nullable=False)
    added_at = Column(DateTime, server_default=func.now())
    articles = relationship("Article", secondary=Article_has_Media, back_populates="medias")

    def __repr__(self):
        return f"<Media(hash={self.sha256}>"
