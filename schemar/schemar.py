from schemar.grammar import *
from schemar.models import (Table, Relation, AttributeAlias)
from schemar.generators.mysql import MysqlGenerator
from collections import OrderedDict
from pyparsing import ParseException


class Schemar:

    def __init__(self):
        self.schema = OrderedDict()

    def define_table(self, *tables, overwrite=False):
        table_list = [Table(table_name)
                      for table_name
                      in tables if
                      table_name not in self.schema or overwrite]

        for table in table_list:
            self.schema[table.name] = table

        return table_list

    def define_relationship(self, source_table, dest_table, type, alias=None):
        self.schema[source_table].add_relation(type, self.schema[dest_table], alias)

    def commit(self):
        generator = MysqlGenerator()
        schema_output = []
        constraint_output = []
        tables = self.schema.copy()

        for _, table in self.schema.items():
            #Add "id" as primary key to defined tables
            table.add_column("id", AttributeAlias("auto"), False)
            table.add_primary_key("id")

            jct_tables = table.generate_junction_tables()

            [jct_table.create_relation_attributes() for jct_table in jct_tables.values()]
            table.create_relation_attributes()

            #Add junction tables to list of tables to be generated
            tables.update(jct_tables)

        for table in tables.values():
            table_output, table_constraints = generator.generate_create_table(table)

            schema_output.extend(table_output)
            constraint_output.extend(table_constraints)

            table.clear_relation_attributes()

        schema_output.append('\n'.join(constraint_output))

        return '\n'.join(schema_output)