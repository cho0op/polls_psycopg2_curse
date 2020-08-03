from psycopg2.extras import execute_values

CREATE_POLLS = """CREATE TABLE IF NOT EXISTS polls 
(id SERIAL PRIMARY KEY, title TEXT, owner_username TEXT);"""
CREATE_OPTIONS = """CREATE TABLE IF NOT EXISTS options 
(id SERIAL PRIMARY KEY, option_text TEXT, poll_id INTEGER, FOREIGN KEY (poll_id) REFERENCES polls (id));"""
CREATE_VOTES = """CREATE TABLE IF NOT EXISTS votes 
(username TEXT, option_id INTEGER, FOREIGN KEY (option_id) REFERENCES options(id));"""

SELECT_ALL_POLLS = "SELECT * FROM pols"
SELECT_POLL_WITH_OPTION = "SELECT * FROM pols JOIN options ON polls.id=options.poll_id WHERE polls.id=%s"

INSERT_OPTION = "INSERT INTO options (option_text, poll_id) VALUES (%s)"  # (option_text, poll_id) goes as one tuple
INSERT_VOTE = "INSERT INTO votes (username, option_id) VALUES (%s, %s)"


def create_tables():
    pass


def create_poll(connection, title, owner_username, options):
    with connection:
        with connection.cursor as cursor:
            cursor.execute("INSERT INTO polls (title, owner_username) VALUES (%s, %s) RETURNING id;",
                           (title, owner_username))
            poll_id = cursor.fetchone()[0]
            poll_options = [(option_text, poll_id) for option_text in options]
            execute_values(cursor, "INSERT INTO options (option_text, poll_id) VALUES (%s);", poll_options)
            # for poll_option in poll_options:
            #     cursor.execute("INSERT INTO options (option_text, poll_id) VALUES (%s);", poll_option)


def get_polls():
    pass


def get_poll_detail():
    pass


def add_poll_vote():
    pass


def get_poll_and_vote_results(connection, id):
    pass


def get_random_poll_vote(connection, id):
    pass
