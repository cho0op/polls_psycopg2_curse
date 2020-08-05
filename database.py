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

TOP_VOTED_OPTION_FROM_EVERY_POLL = """Select 
 DISTINCT ON (options.poll_id) poll_id, 
 options.id, options.option_text, 
 options.poll_id,
 COUNT(votes.option_id) as vote_count
  FROM options 
  JOIN votes ON options.id=votes.option_id 
  GROUP BY options.id ORDER BY options.poll_id, vote_count DESC;"""


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
            # replaced by execute_values
            # for poll_option in poll_options:
            #     cursor.execute("INSERT INTO options (option_text, poll_id) VALUES (%s);", poll_option)


def get_latest_poll(connection):
    with connection:
        with connection.cursor as cursor:
            cursor.execute("SELECT * FROM polls"
                           "JOIN options ON polls.id=options.poll_id "
                           "WHERE polls.id = ("
                           "SELECT id FROM polls ORDER BY id DESC LIMIT 1)")
            return cursor.fetchall()


def get_polls():
    pass


def get_poll_detail():
    pass


def add_poll_vote():
    pass


def get_poll_and_vote_results(connection, poll_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT "
                "options.id,"
                "options.option_text,"
                "COUNT(options.id),"
                "COUNT(options.id)/SUM(COUNT(options.id)) OVER() *100.0"
                # OVER(), window function. As I understand it allows us to SUM COUNT'ed after all rows were processed. 
                # Because window function runs after COUNT were evaluated
                "FROM options JOIN votes ON options.id=votes.option_id"
                " WHERE options.poll_id=%s"
                "GROUP BY options.id", (poll_id,)
            )
            return cursor.fetchall()


def get_random_poll_vote(connection, option_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM votes WHERE option_id=%s ORDER BY RANDOM() LIMIT 1", (option_id,))
            return cursor.fetcone()
