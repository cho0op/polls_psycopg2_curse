from typing import List

from connections import create_connection, connection_pool
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
        connection = connection_pool.getconn()
        new_option_id = database.add_option(connection, self.text, self.poll_id)
        connection_pool.putconn(connection)
        self.id = new_option_id

    def vote(self, username: str):
        connection = connection_pool.getconn()
        database.add_poll_vote(connection, username, self.id)
        connection_pool.putconn(connection)

    @property
    def votes(self) -> List[database.Vote]:
        connection = connection_pool.getconn()
        votes = database.get_votes_for_option(connection, self.id)
        connection_pool.putconn(connection)
        return votes

    @classmethod
    def get(cls, option_id: int) -> "Option":
        connection = connection_pool.getconn()
        option = database.get_option(connection, option_id)
        connection_pool.putconn(connection)
        return cls(option[1], option[2], option[0])
