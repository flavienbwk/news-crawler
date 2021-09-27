import os
from typing import Union

import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.base import base

FILE_PATH = os.path.realpath(__file__)
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
SQLITE_DATABASE = f"{DIR_PATH}/../../database/news.sqlite"

AUTHORIZED_CONNECTORS = ["postgresql", "sqlite"]


class Database:
    def __init__(self, connector: str) -> None:
        if connector not in AUTHORIZED_CONNECTORS:
            raise ValueError(f"'{connector}' is not a supported connector !")
        self.connector = connector
        self.session: Union[sessionmaker, None] = None
        self.db = None

    def getSession(self) -> Union[sessionmaker, None]:
        return self.session

    def isDatabaseAvailable(self) -> bool:
        if self.connector == "postgresql":
            return self._isPostgresDatabaseAvailable()
        if self.connector == "sqlite":
            return self._isSQLiteDatabaseAvailable()
        return False

    def initDatabase(self) -> None:
        if self.connector == "postgresql":
            return self._initPostgresDatabase()
        if self.connector == "sqlite":
            return self._initSQLiteDatabase()
        raise ValueError("initDatabase: Could not find valid database")

    def _isPostgresDatabaseAvailable(self) -> bool:
        try:
            conn = psycopg2.connect(
                "host='{}' dbname='{}' user='{}' password='{}'".format(
                    os.environ.get("POSTGRES_HOST"),
                    os.environ.get("POSTGRES_DB"),
                    os.environ.get("POSTGRES_USER"),
                    os.environ.get("POSTGRES_PASSWORD"),
                )
            )
            conn.close()
            return True
        except psycopg2.OperationalError:
            return False

    def _isSQLiteDatabaseAvailable(self) -> bool:
        return False if self.db.closed else True

    def _initPostgresDatabase(self):
        self.db = create_engine(
            "postgresql://{}:{}@{}/{}".format(
                os.environ.get("POSTGRES_USER"),
                os.environ.get("POSTGRES_PASSWORD"),
                os.environ.get("POSTGRES_HOST"),
                os.environ.get("POSTGRES_DB"),
            )
        )
        session = sessionmaker(self.db)
        self.session = session()
        base.metadata.create_all(self.db)

    def _initSQLiteDatabase(self):
        self.db = create_engine(f"sqlite:///{SQLITE_DATABASE}")
        session = sessionmaker(self.db)
        self.session = session()
        base.metadata.create_all(self.db)

    def save_changes(self, data=None, commit=False):
        """
        Persists data to the database.

        Don't use `data` if you .delete()
        """
        try:
            if data is not None:
                self.session.add(data)
            if commit:
                self.session.commit()
            return True
        except Exception as e:
            print(e, flush=True)
            return False
