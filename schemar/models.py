from collections import OrderedDict

class Table:
    def __init__(self, name):
        self.name = name
        self.columns = OrderedDict()
        self.relations = OrderedDict()

        self.relation_attributes = OrderedDict()
        self.foreign_keys = OrderedDict()
        self.primary_keys = set()

    def add_column(self, name, data_type, last=True):
        self.columns[name] = Column(name, data_type)
        self.columns.move_to_end(name, last)

    def add_relation(self, type, dest_table, alias=None):
        self.relations[dest_table] = Relation(type, dest_table, alias)

    def add_primary_key(self, col_name):
        self.primary_keys.add(col_name)

    def has_relation_with(self, dest_table, type):
        return dest_table in self.relations and self.relations[dest_table].type == type

    def get_relations(self):
        return self.relations.values()

    def create_relation_attributes(self):
        for relation in self.get_relations():
            dest_table = relation.dest_table
            if relation.type == Relation.HAS_ONE:
                field_name = "{0}_id".format(relation.alias)

                self.relation_attributes[field_name] = Column(field_name, AttributeAlias("int"))
                self.foreign_keys[field_name] = dest_table

                if dest_table is not self and dest_table.has_relation_with(self, Relation.HAS_ONE):
                    #One-To-One Relation
                    self.relation_attributes[field_name].unique = True
            else:
                if not dest_table.has_relation_with(self, Relation.HAS_MANY):
                    #Has-Many Relation
                    field_name = "{0}_id".format(self.name)
                    dest_table.relation_attributes[field_name] = Column(field_name, AttributeAlias("int"))
                    dest_table.foreign_keys[field_name] = self

    def clear_relation_attributes(self):
        self.relation_attributes = {}
        self.foreign_keys = {}

    def generate_junction_tables(self):
        junction_tables = OrderedDict()

        for relation in self.get_relations():
            dest_table = relation.dest_table
            if relation.type == Relation.HAS_MANY and dest_table.has_relation_with(self, Relation.HAS_MANY):
                #Many-Many-Relation

                #Keeps order of the tables consistent, prevents multiple junction tables
                linked_tables = [self.name, dest_table.name]
                linked_tables.sort()

                table_name = "{0}_{1}_link".format(*linked_tables)
                junction_table = Table(table_name)
                junction_table.add_relation(Relation.HAS_ONE, self)
                junction_table.add_relation(Relation.HAS_ONE, dest_table)

                junction_tables[table_name] = junction_table

        return junction_tables

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return "Table('%s') \n Columns: %s" % (self.name, "\n".join(self.columns))

    def __repr__(self):
        return self.__str__()


class Column:
    def __init__(self, name, data_type, unique=False):
        self.name = name
        self.data_type = data_type
        self.unique = unique

    def __str__(self):
        return "Column('%s') %s" % (self.name, self.data_type)

    def __repr__(self):
        return self.__str__()


class AttributeAlias():
    def __init__(self, alias):
        self.alias = alias


class Relation:
    HAS_ONE = 0
    HAS_MANY = 1

    def __init__(self, type, dest_table, alias):
        self.type = type
        self.dest_table = dest_table

        if alias is None:
            self.alias = dest_table.name
        else:
            self.alias = alias

