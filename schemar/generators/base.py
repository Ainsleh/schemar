from schemar.models import AttributeAlias


class BaseSQLGenerator:
    constraint_tpl = (
        """ALTER TABLE {source_table} ADD CONSTRAINT {constraint_name}
        FOREIGN KEY ({field}) REFERENCES {target_table} ({references_field})
        ON DELETE CASCADE ON UPDATE CASCADE;"""
    )

    attribute_aliases = {

    }

    def field_quote(self, field_name):
        return "`{0}`".format(field_name)

    def resolve_attribute(self, attribute):
        if isinstance(attribute, AttributeAlias):
            return self.attribute_aliases[attribute.alias]
        else:
            return attribute

    def table_create_suffix(self):
        return ''

    def generate_create_table(self, table):
        table_output = []
        col_output = []
        table_constraints = []

        attributes = table.columns.copy()
        attributes.update(table.relation_attributes)
        table_output.append("CREATE TABLE {0} (".format(self.field_quote(table.name)))

        #Write columns
        for col_name, column in attributes.items():
            col_output.append("\t {0} {1}{2}".format(
                self.field_quote(column.name),
                self.resolve_attribute(column.data_type),
                " UNIQUE" if column.unique else ""
            ))

        #Write primary key definitions
        if len(table.primary_keys) > 0:
            col_output.append("\t PRIMARY KEY({0})".format(
                ', '.join([self.field_quote(pk) for pk in table.primary_keys])))

        #Join column outputs
        for i, col in enumerate(col_output):
            table_output.append("{0}{1}".format(col, ',' if i < len(col_output) - 1 else ''))

        #Generate foreign key constraints
        fk_count = 0
        for field_name, target_table in table.foreign_keys.items():
            constraint_name = "{0}_fk_{1}".format(table.name, fk_count)
            table_constraints.append(
                self.constraint_tpl.format(
                    source_table=table.name,
                    fk_count=fk_count,
                    field=field_name,
                    constraint_name=self.field_quote(constraint_name),
                    references_field=self.field_quote("id"),
                    target_table=self.field_quote(target_table.name)
                )
            )
            fk_count += 1

        table_output.append(") {0};".format(self.table_create_suffix()))

        return table_output, table_constraints