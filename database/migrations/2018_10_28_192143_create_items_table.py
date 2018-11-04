from orator.migrations import Migration


class CreateItemsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('items') as table:
            table.increments('id')
            table.string('title').unique()
            table.text('description')
            table.string('slug').unique()

            table.integer('category_id').unsigned()
            table.integer('user_id').unsigned()

            table.foreign('category_id').references('id').on('categories').on_delete('cascade')
            table.foreign('user_id').references('id').on('users').on_delete('cascade')

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('items')
