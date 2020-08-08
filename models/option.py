from typing import List

from connections import create_connection
import database


class Option:
    def __init__(self, option_text: str, poll_id: int, _id: int = None):
        self.option_text = option_text
        self.poll_id = poll_id
        self.id = _id

    def __repr__(self):
        return f"Option({self.id}, {self.option_text}, {self.poll_id})"

    def save(self):
        connection = create_connection()
        new_option_id = database.add_option(connection, self.option_text, self.poll_id)
        connection.close()
        self.id = new_option_id

    def vote(self, username: str):
        connection = create_connection()
        database.add_poll_vote(connection, username, self.id)
        connection.close()

    @property
    def votes(self) -> List[database.Vote]:
        connection = create_connection()
        votes = database.get_votes_for_option(connection, self.id)
        connection.close()
        return votes

    @classmethod
    def get(cls, option_id):
        connection = create_connection()
        option = database.get_option(connection, option_id)
        connection.close()
        return cls(option[1], option[2], option[1])
