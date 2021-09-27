import time
from typing import Union

from models.Article import Article
from models.Media import Media
from sqlalchemy import exc

from utils import Logger
from utils.Database import Database

LOGGER = Logger.Logger()


class Persister:
    def __init__(
        self,
        database: Database,
        batch_size: int = -1,  # Number of objects to be inserted at the same time
    ) -> None:
        if batch_size == 0:
            raise ValueError("Batch size can't be == 0")
        self.session = database.getSession()
        self.batch_size = batch_size
        self.objects = []

    def add_object(self, object: Union[Article, Media]):
        self.objects.append(object)
        self.add_object_to_session(object)

    def add_object_to_session(self, object: Union[Article, Media]):
        self.session.add(object)

    def request_save_objects(self):
        """Save previously added objects only if the number
        of objects to save is >= self.batch_size.
        """
        if len(self.objects) >= self.batch_size:
            self.save_objects()

    def save_objects(self):
        """Instantly save previously added objects."""
        wait_time = 0
        nb_tries = 5
        while nb_tries:
            time.sleep(wait_time)
            try:
                self.session.commit()
                break
            except exc.IntegrityError:
                self.session.rollback()
                LOGGER.warning(f"Item(s) already in database")
                break
            except exc.OperationalError:
                self.session.rollback()
                nb_tries -= 1
                LOGGER.warning(
                    f"Database is locked ! Retrying in 3 seconds ({nb_tries} tries left)"
                )
                for object in self.objects:
                    self.add_object_to_session(object)
                wait_time = 0
        self.objects = []
