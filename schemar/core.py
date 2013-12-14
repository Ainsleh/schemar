import argparse
import readline

from pyparsing import ParseException
from textwrap import dedent
from termcolor import colored

from schemar.models import Relation
from schemar.grammar import *
from schemar.schemar import Schemar
from schemar.generators import generators


OVERWRITE_WARNING = colored("Warning: You will be overwriting an already defined table", "red", attrs=["bold"])
HELP_MESSAGE = """
    The following commands are available:
    Define table:
        def {table_name}
    Define has one relationship:
        {source_table} has one {destination_table}
    Define has many relationship:
        {source table} has many {destination_table}

    Tables which do not exist are automatically created when you define a relationship.
    """


def main():
    schemar = Schemar()

    def define_relationship(source_table, dest_table, type, alias):
        get_table_columns(*schemar.define_table(source_table, dest_table))
        schemar.define_relationship(source_table, dest_table, type, alias)

    def define_has_one(str, loc, tok):
        source_table, _, dest_table, alias = tok
        define_relationship(source_table, dest_table, Relation.HAS_ONE, alias)

    def define_has_many(str, loc, tok):
        source_table, _, dest_table, alias = tok
        define_relationship(source_table, dest_table, Relation.HAS_MANY, alias)

    def handle_define_table(str, loc, tok):
        _, name = tok

        if schemar.contains_table(name):
            print("\n" + OVERWRITE_WARNING + "\n")

        table_list = schemar.define_table(name, overwrite=True)
        get_table_columns(*table_list)

    def handle_commit(str, loc, tok):
        _, output_file, generator_name = tok

        if generator_name in generators:
            generator = generators[generator_name]
            generated_schema = schemar.commit(generator)

            f = open(output_file, 'w')
            f.write(generated_schema)
            f.close()
        else:
            print("Output format not recognised, accepted values are ({0})".format(", ".join(generators.keys())))

    def handle_peek(str, loc, tok):
        print(schemar.commit())

    def display_help(str, loc, tok):
        print(dedent(HELP_MESSAGE.strip()))

    has_one_grammar.setParseAction(define_has_one)
    has_many_grammar.setParseAction(define_has_many)

    def_grammar.setParseAction(handle_define_table)
    commit_grammar.setParseAction(handle_commit)
    peek_grammar.setParseAction(handle_peek)

    help_grammar.setParseAction(display_help)

    print_welcome_message()
    while True:
        try:
            input_str = input('Schemar> ')
            if input_str == "exit":
                break
            else:
                command_grammar.parseString(input_str)
        except ParseException:
            print("Unrecognised command. Try again.")


def print_welcome_message():
    print()


def get_table_columns(*tables):
    for table in tables:
        print("Defining attributes for table: {0}".format(table.name))
        while True:
            try:
                input_str = input("\tField -> ")
                if input_str == "" or input_str == "done":
                    break
                else:
                    name, data_type = column_def_grammar.parseString(input_str)

                    table.add_column(name, data_type)

            except ParseException:
                print("Incorrect attribute definition. Try format \"<name> <data_type>\"")