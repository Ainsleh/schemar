from schemar.models import Relation
from schemar.grammar import *
from schemar.schemar import Schemar

def main():
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


    schemar = Schemar()
    schemar.define_table("person")
    schemar.define_relationship("person", "person", Relation.HAS_ONE, "parent")
    #define_relationship("author", "book", Relation.HAS_MANY, "writer")
    #define_relationship("book", "author", Relation.HAS_MANY)
    #define_relationship("book", "publisher", Relation.HAS_ONE)
    print(schemar.commit())

# while True:
#     try:
#         input_str = input(': ')
#         if input_str == "Quit":
#             break
#         else:
#             command_grammar.parseString(input_str)
#     except ParseException:
#         print("Unrecognised command. Try again.")