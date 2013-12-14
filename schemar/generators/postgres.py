from schemar.generators.base import BaseSQLGenerator


class PostgresGenerator(BaseSQLGenerator):
    attribute_aliases = {
        "auto": "serial",
        "int": "integer",
        "bool": "boolean",
        "string": "varchar(128)",
        "time": "time",
        "timestamp": "timestamp",
        "date": "date"
    }

    def field_quote(self, field_name):
        return field_name

    def table_create_suffix(self):
        return ""