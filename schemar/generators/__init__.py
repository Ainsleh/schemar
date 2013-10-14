from schemar.generators.mysql import MysqlGenerator
from schemar.generators.postgres import PostgresGenerator

generators = {
    'mysql': MysqlGenerator(),
    'postgres': PostgresGenerator()
}