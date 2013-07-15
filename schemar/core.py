from pyparsing import *
from schemar.models import (Table, Relation, AttributeAlias)
from schemar.grammar import *
from schemar.generators.mysql import MysqlGenerator
from collections import OrderedDict


class Schemar:
    schema = OrderedDict()

    def define_table(self, *tables, overwrite=False):
        table_list = [Table(table_name)
                      for table_name
                      in tables if
                      table_name not in self.schema or overwrite]

        for table in table_list:
            self.schema[table.name] = table

        return table_list

    def define_relationship(self, source_table, dest_table, type, alias=None):
        self.define_table(source_table, dest_table)
        self.schema[source_table].add_relation(type, self.schema[dest_table], alias)

    def commit(self):
        generator = MysqlGenerator()
        schema_output = []
        constraint_output = []
        tables = set(self.schema.values())

        for _, table in self.schema.items():
            #Add "id" as primary key to defined tables
            table.add_column("id", AttributeAlias("auto"))
            table.add_primary_key("id")

            jct_tables = table.generate_junction_tables()

            [jct_table.create_relation_attributes() for jct_table in jct_tables]
            table.create_relation_attributes()

            #Add junction tables to list of tables to be generated
            tables |= jct_tables

        for table in tables:
            table_output, table_constraints = generator.generate_create_table(table)

            schema_output.extend(table_output)
            constraint_output.extend(table_constraints)

            table.clear_relation_attributes()

        schema_output.append('\n'.join(constraint_output))
        print('\n'.join(schema_output))

    def get_table_columns(self, *tables):
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


def main():
    schemar = Schemar()

    def define_has_one(str, loc, tok):
        source_table, _, dest_table, alias = tok
        schemar.define_relationship(source_table, dest_table, Relation.HAS_ONE, alias)

    def define_has_many(str, loc, tok):
        source_table, _, dest_table, alias = tok
        schemar.define_relationship(source_table, dest_table, Relation.HAS_MANY, alias)

    def handle_define_table(str, loc, tok):
        _, name = tok
        table_list = schemar.define_table(name, True)
        schemar.get_table_columns(table_list)

    def handle_commit(str, loc, tok):
        schemar.commit()

    def_grammar.setParseAction(handle_define_table)
    has_one_grammar.setParseAction(define_has_one)
    has_many_grammar.setParseAction(define_has_many)
    commit_grammar.setParseAction(handle_commit)

    schemar.define_table("person")
    schemar.define_relationship("person", "person", Relation.HAS_ONE, "parent")
    #define_relationship("author", "book", Relation.HAS_MANY, "writer")
    #define_relationship("book", "author", Relation.HAS_MANY)
    #define_relationship("book", "publisher", Relation.HAS_ONE)
    schemar.commit()

    # while True:
    #     try:
    #         input_str = input(': ')
    #         if input_str == "Quit":
    #             break
    #         else:
    #             command_grammar.parseString(input_str)
    #     except ParseException:
    #         print("Unrecognised command. Try again.")