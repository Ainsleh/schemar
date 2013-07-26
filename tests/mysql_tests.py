import unittest
import os
import sys

TESTS_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.realpath(os.path.join(TESTS_ROOT, '..')))

from schemar.schemar import Schemar
from schemar.models import (Relation, AttributeAlias)


class SchemarMysqlTests(unittest.TestCase):
    def test_comment_schema(self):
        schemar = Schemar()
        schemar.define_table("comment")

        comment_table = schemar.schema["comment"]
        comment_table.add_column("author", AttributeAlias("string"))
        comment_table.add_column("body", AttributeAlias("string"))
        schemar.define_relationship("comment", "comment", Relation.HAS_ONE, "parent")

        self.assertFixtureEqual("comment_schema", schemar.commit())

    def test_library_schema(self):
        schemar = Schemar()
        schemar.define_table("author", "book", "publisher")

        author_table = schemar.schema["author"]
        author_table.add_column("name", AttributeAlias("string"))

        book_table = schemar.schema["book"]
        book_table.add_column("title", AttributeAlias("string"))
        book_table.add_column("ISBN", AttributeAlias("int"))

        publisher_table = schemar.schema["publisher"]
        publisher_table.add_column("name", AttributeAlias("string"))

        schemar.define_relationship("author", "book", Relation.HAS_MANY)
        schemar.define_relationship("book", "author", Relation.HAS_MANY)
        schemar.define_relationship("book", "publisher", Relation.HAS_ONE)

        self.assertFixtureEqual("library_schema", schemar.commit())

    def assertFixtureEqual(self, fixture_name, actual_output):
        fixture_file = os.path.join(TESTS_ROOT, "fixtures", fixture_name)
        with open(fixture_file) as f:
            expected_output = f.read().strip()
            self.assertEqual(actual_output, expected_output)


if __name__ == '__main__':
    unittest.main()