import csv

from django.conf import settings
from django.core.management import BaseCommand

from recipes.models import (
    Tag,
    Ingredient,
)


class Command(BaseCommand):
    help = 'Import data from CSV files'

    def add_arguments(self, parser):
        parser.add_argument('--folder',
                            type=str,
                            help='Path to folder containing CSV files')

    def handle(self, *args, **options):
        csv_folder = options['folder'] or settings.CSV_FOLDER
        ingredient_file = f'{csv_folder}/ingredients.csv'
        tag_file = f'{csv_folder}/tags.csv'

        self.import_ingredients(ingredient_file)
        self.import_tags(tag_file)

    def import_ingredients(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                name, measurement_unit = row
                Ingredient.objects.get_or_create(
                    name=name,
                    measurement_unit=measurement_unit,
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Imported Ingredient: {name}'
                    )
                )

    def import_tags(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                name, color, slug = row
                Tag.objects.get_or_create(
                    name=name,
                    color=color,
                    slug=slug,
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Imported Tag: {name}'
                    )
                )
