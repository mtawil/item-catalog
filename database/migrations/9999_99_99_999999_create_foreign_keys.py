from orator.migrations import Migration


class CreateForeignKeys(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('items') as table:
            table.foreign('category_id').references('id').on('categories').on_delete('cascade')
            table.foreign('user_id').references('id').on('users').on_delete('cascade')

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('users')
