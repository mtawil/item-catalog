from orator.migrations import Migration


class CreateCategoriesTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('categories') as table:
            table.increments('id')
            table.string('title').unique()
            table.string('slug').unique()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('categories')
