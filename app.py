from typing import List
import random

import database

from models.option import Option
from models.poll import Poll
from connections import create_connection, pool_handler

DATABASE_PROMPT = "Enter new db URI or leave empty if you take it from .env"
MENU = """--MENU--
1) Create poll
2) View polls
3) Vote on a poll
4) Show poll Votes
5) Select random winner from poll option
6) Exit

Your choice: """

NEW_OPTION_PROMPT = "Enter new option (or leave empty to stop adding options)"


def prompt_create_poll():
    poll_title = input("Input poll title: ")
    poll_owner = input("input poll owner: ")
    poll = Poll(poll_title, poll_owner)
    poll.save()
    while new_option := input(NEW_OPTION_PROMPT):
        poll.add_option(new_option)


def list_open_polls():
    polls = Poll.all()
    for poll in polls:
        print(poll)


def prompt_vote_poll():
    poll_id = int(input("Enter poll would you like to vote: "))
    poll = Poll.get(poll_id)
    poll_options = poll.options
    print_poll_options(poll_options)
    users_choice = int(input("Now choice the option: "))
    option = Option.get(users_choice)
    users_name = input("Enter your name: ")
    option.vote(users_name)


def print_poll_options(poll_options: List[Option]):
    for poll_option in poll_options:
        print(poll_option)


def show_poll_votes():
    poll_id = int(input("Input id of poll you would like to see: "))
    poll = Poll.get(poll_id)
    options = poll.options
    votes_for_option = [len(option.votes) for option in options]
    sum_of_votes = sum(votes_for_option)
    try:
        for option, votes in zip(options, votes_for_option):
            vote_percentage = votes / sum_of_votes * 100
            print(f"{option.text} got {votes} ({vote_percentage}% of total)")
    except ZeroDivisionError:
        print("Poll didnt'd get any votes")
    # try:
    #     polls_and_votes = database.get_poll_and_vote_results(connection, poll_id)
    # except DivisionByZero:
    #     print("This poll hasn't votes")
    # else:
    #     for _id, option_text, count, percentage in polls_and_votes:
    #         print(f"{option_text} get {count} votes ({percentage:.2f}% of total)")


def randomize_poll_winner():
    poll_id = int(input("Enter poll you'd like to see a winner for: "))
    poll = Poll.get(poll_id)
    print_poll_options(poll.options)
    option_id = int(input("Input id of option: "))
    option = Option.get(option_id)
    votes = option.votes
    winner = random.choice(votes)
    print(f"winner is {winner[0]}!")


MENU_OPTIONS = {
    "1": prompt_create_poll,
    "2": list_open_polls,
    "3": prompt_vote_poll,
    "4": show_poll_votes,
    "5": randomize_poll_winner
}


def main():
    with pool_handler() as connection:
        database.create_tables(connection)
    while (selection := input(MENU)) != "6":
        try:
            MENU_OPTIONS[selection]()
        except KeyError:
            print("Invalid options")


if __name__ == "__main__":
    main()
