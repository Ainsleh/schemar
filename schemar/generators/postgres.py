from schemar.generators.base import BaseGenerator


class PostgresGenerator(BaseGenerator):
    attribute_aliases = {
        "auto": "serial",
        "int": "integer",
        "bool": "boolean",
        "string": "varchar(128)",
        "time": "time",
        "timestamp": "timestamp",
        "date": "date"
    }

    def table_create_suffix(self):
        return ""