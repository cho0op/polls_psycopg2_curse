import datetime
import pytz
from typing import List

from connections import create_connection, connection_pool, get_cursor
import database


class Option:
    def __init__(self, option_text: str, poll_id: int, _id: int = None):
        self.text = option_text
        self.poll_id = poll_id
        self.id = _id

    def __str__(self):
        return f"{self.id}: {self.text}"

    def __repr__(self):
        return f"Option({self.id}, {self.text}, {self.poll_id})"

    def save(self):
        with get_cursor() as connection:
            new_option_id = database.add_option(connection, self.text, self.poll_id)
            self.id = new_option_id

    def vote(self, username: str):
        with get_cursor() as connection:
            vote_timestamp = datetime.datetime.now(tz=pytz.utc).timestamp()
            database.add_poll_vote(connection, username,  vote_timestamp, self.id)

    @property
    def votes(self) -> List[database.Vote]:
        with get_cursor() as connection:
            votes = database.get_votes_for_option(connection, self.id)
            return votes

    @classmethod
    def get(cls, option_id: int) -> "Option":
        with get_cursor() as connection:
            option = database.get_option(connection, option_id)
            return cls(option[1], option[2], option[0])
