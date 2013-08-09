from pyparsing import ParseException
from schemar.models import Relation
from schemar.grammar import *
from schemar.schemar import Schemar
import argparse

def main():
    parser = argparse.ArgumentParser(description='A CLI Tool to generate SQL schemas quickly')
    parser.add_argument('output_file', metavar='filename',
                   help='The file to which the generated SQL schema will be written')
    args = parser.parse_args()

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
        table_list = schemar.define_table(name)
        get_table_columns(*table_list)

    def handle_commit(str, loc, tok):
        generated_schema = schemar.commit()
        f = open(args.output_file, 'w')
        f.write(generated_schema)
        f.close()

    def_grammar.setParseAction(handle_define_table)
    has_one_grammar.setParseAction(define_has_one)
    has_many_grammar.setParseAction(define_has_many)
    commit_grammar.setParseAction(handle_commit)

    while True:
        try:
            input_str = input(': ')
            if input_str == "exit":
                break
            else:
                command_grammar.parseString(input_str)
        except ParseException:
            print("Unrecognised command. Try again.")


def get_table_columns(*tables):
    for table in tables:
        print("Defining attributes for table: {0}".format(table.name))
        while True:
            try:
                input_str = input("\t-> ")
                if input_str == "":
                    break
                else:
                    name, data_type = column_def_grammar.parseString(input_str)

                    table.add_column(name, data_type)

            except ParseException:
                print("Incorrect attribute definition. Try format \"<name> <data_type>\"")