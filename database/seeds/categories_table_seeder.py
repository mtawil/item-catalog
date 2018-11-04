from orator.seeds import Seeder
from app.models.category import Category


class CategoriesTableSeeder(Seeder):

    def run(self):
        """
        Run the database seeds.
        """
        categories = [
            "Soccer",
            "Basketball",
            "Baseball",
            "Frisbee",
            "Snowboarding",
            "Rock Climbing",
            "Football",
            "Skating",
            "Hockey"
        ]

        for category in categories:
            Category.create(title=category)
