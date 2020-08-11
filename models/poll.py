import database
from typing import List
from models.option import Option
from connections import create_connection, connection_pool, get_cursor


class Poll:
    def __init__(self, title: str, owner: str, _id: int = None, ):
        self.id = _id
        self.title = title
        self.owner = owner

    def __str__(self):
        return f"{self.id}: {self.title} (created by {self.owner})"

    def __repr__(self):
        return f"Poll({self.id}, {self.title}, {self.owner})"

    def save(self):
        # connection = connection_pool.getconn()
        # Instead of creating connection every time, we take it from the connection pool
        # connection = create_connection()
        # connection.close()
        # connection_pool.putconn(connection)
        with get_cursor() as connection:
            new_poll_id = database.create_poll(connection, self.title, self.owner)
            self.id = new_poll_id

    def add_option(self, option_text: str):
        Option(option_text, self.id).save()

    @property
    def options(self) -> List[Option]:
        with get_cursor() as connection:
            options = database.get_poll_options(connection, self.id)
            return [Option(option[1], option[2], option[0]) for option in options]

    @classmethod
    def get(cls, poll_id: int) -> "Poll":
        with get_cursor() as connection:
            poll = database.get_poll(connection, poll_id)
            return cls(poll[1], poll[2], poll[0])

    @classmethod
    def all(cls) -> List["Poll"]:
        with get_cursor() as connection:
            polls = database.get_polls(connection)
            return [cls(poll[1], poll[2], poll[0]) for poll in polls]

    @classmethod
    def latest(cls) -> "Poll":
        with get_cursor() as connection:
            poll = database.get_latest_poll(connection)
            return cls(poll[1], poll[2], poll[0])
