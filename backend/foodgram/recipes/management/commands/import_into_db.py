import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient

HELP_MESSAGE = 'Импорт данных из data/ingredients.csv'
START_MESSAGE = 'Начинаем импорт...'
STOP_MESSAGE = 'Импорт закончен...'
IMPORT_ERROR = 'Что-то пошло не так: {error}.'
IMPORT_MESSAGE = 'Обрабатывается набор данных: {data}'
# PATH_TO_CSV_FILES = '../../data/ingredients.csv'
# Для сборки Docker образа указать так
PATH_TO_CSV_FILES = 'ingredients.csv'


class Command(BaseCommand):
    """
    Класс для работы managment комманды.
    Импорт информации из csv файла в модель Ingredient.
    python manage.py import_into_db
    """

    help = HELP_MESSAGE

    def handle(self, *args, **options):
        print(START_MESSAGE)
        try:
            with open(PATH_TO_CSV_FILES, encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    print(IMPORT_MESSAGE.format(data=row))
                    name, measurement_unit = row
                    Ingredient.objects.get_or_create(
                        name=name, measurement_unit=measurement_unit
                    )
        except Exception as error:
            print(IMPORT_ERROR.format(error=error))

        finally:
            print(STOP_MESSAGE)
