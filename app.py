import os
from typing import List

import psycopg2
from psycopg2.errors import DivisionByZero
from dotenv import load_dotenv
import database

DATABASE_PROMPT = "Enter new db URI or leave empty if you take it from .env"
MENU = """--MENU--
1) Create poll
2) View polls
3) Vote on a poll
4) Show poll Votes
5) Select random winner fron poll option
6) Exit

Your choice: """

NEW_OPTION_PROMPT = "Enter new option (or leave empty to stop adding options)"


def prompt_create_poll(connection):
    poll_title = input("Input poll title: ")
    poll_owner = input("input poll owner: ")
    options = []
    while new_option := input(NEW_OPTION_PROMPT):
        options.append(new_option)
    database.create_poll(connection, poll_title, poll_owner, options)


def list_open_polls(connection):
    polls = database.get_polls()
    for poll in polls:
        print(f"poll id: {poll[0]}, poll title: {poll[1]}, poll owner: {poll[2]}\n")


def prompt_vote_poll(connection):
    poll_id = int(input("Enter poll would you like to vote: "))
    poll_options = database.get_poll_detail()
    print_poll_options(poll_options)
    users_choice = input("Now choice the option: ")
    users_name = input("Enter your name: ")
    database.add_poll_vote()


def print_poll_options(poll_options: List[database.PollWithOption]):
    for poll_option in poll_options:
        print(f"{poll_option[0]} : {poll_option[1]}")


def show_poll_votes(connection):
    poll_id = input("Input id of poll you would like to see: ")
    try:
        polls_and_votes = database.get_poll_and_vote_results(connection, poll_id)
    except DivisionByZero:
        print("This poll hasn't votes")
    else:
        for _id, option_text, count, percentage in polls_and_votes:
            print(f"{option_text} get {count} votes ({percentage:.2f}% of total)")


def randomize_poll_winner(connection):
    poll_id = int(input("Enter poll you'd like to see a winner for: "))
    poll_options = database.get_poll_details(connection, poll_id)
    print_poll_options(poll_options)
    option_id = input("Input id of option: ")
    winner = database.get_random_poll_vote(connection, id)
    print(f"winner is {winner}!")


MENU_OPTIONS = {
    "1": prompt_create_poll,
    "2": list_open_polls,
    "3": prompt_vote_poll,
    "4": show_poll_votes,
    "5": randomize_poll_winner
}


def main():
    load_dotenv()
    database_uri = os.environ["DATABASE_URI"]
    connection = psycopg2.connect(database_uri)
    database.create_tables()
    while (selection := input(MENU)) != "6":
        try:
            MENU_OPTIONS[selection](connection)
        except KeyError:
            print("Invalid options")


if __name__ == "__main__":
    main()
