from orator.seeds import Seeder
from .categories_table_seeder import CategoriesTableSeeder


class DatabaseSeeder(Seeder):

    def run(self):
        """
        Run the database seeds.
        """
        self.call(CategoriesTableSeeder)

