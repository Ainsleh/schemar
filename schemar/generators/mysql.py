from schemar.generators.base import BaseSQLGenerator


class MysqlGenerator(BaseSQLGenerator):
    attribute_aliases = {
        "auto": "int(11) AUTO_INCREMENT",
        "int": "int(11)",
        "bool": "bool",
        "string": "varchar(128)",
        "time": "time",
        "timestamp": "timestamp",
        "date": "date",
        "datetime": "datetime"
    }

    def table_create_suffix(self):
        return "ENGINE=InnoDB DEFAULT CHARSET=utf8"