import csv
import os

from django.conf import settings
from django.core.management import BaseCommand

from reviews.models import Category, Comment, Genre, Title, Review, Genre_Title
from users.models import CustomUser


DB_PATH = os.path.join(settings.BASE_DIR, 'db.sqlite3')


class Command(BaseCommand):
    help = 'description'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear all tables in data base.'
        )

    def categories_load(self):
        file_path = 'static/data/category.csv'
        with open(file_path, "r") as csv_file:
            data = list(csv.DictReader(csv_file, delimiter=","))
            Category.objects.bulk_create([Category(**row) for row in data])

    def genres_load(self):
        file_path = 'static/data/genre.csv'
        with open(file_path, "r") as csv_file:
            data = list(csv.DictReader(csv_file, delimiter=","))
            Genre.objects.bulk_create([Genre(**row) for row in data])

    def users_load(self):
        file_path = 'static/data/users.csv'
        with open(file_path, "r") as csv_file:
            data = list(csv.DictReader(csv_file, delimiter=","))
            CustomUser.objects.bulk_create([CustomUser(**row) for row in data])

    def titles_load(self):
        file_path = 'static/data/titles.csv'
        with open(file_path, "r") as csv_file:
            data = list(csv.DictReader(csv_file, delimiter=","))
            Title.objects.bulk_create([Title(
                id=row['id'],
                name=row['name'],
                year=row['year'],
                category=Category.objects.get(pk=row['category'])
            ) for row in data])

    def reviews_load(self):
        file_path = 'static/data/review.csv'
        with open(file_path, "r") as csv_file:
            data = list(csv.DictReader(csv_file, delimiter=","))
            Review.objects.bulk_create([
                Review(
                    id=row['id'],
                    title=Title.objects.get(pk=row['title_id']),
                    text=row['text'],
                    author=CustomUser.objects.get(pk=row['author']),
                    score=row['score'],
                    pub_date=row['pub_date']
                )
                for row in data
            ])

    def comments_load(self):
        file_path = 'static/data/comments.csv'
        with open(file_path, "r") as csv_file:
            data = list(csv.DictReader(csv_file, delimiter=","))
            Comment.objects.bulk_create([
                Comment(
                    id=row['id'],
                    review=Review.objects.get(pk=row['review_id']),
                    text=row['text'],
                    author=CustomUser.objects.get(pk=row['author']),
                    pub_date=row['pub_date']
                )
                for row in data
            ])

    def genre_title_load(self):
        file_path = 'static/data/genre_title.csv'
        with open(file_path, "r") as csv_file:
            data = list(csv.DictReader(csv_file, delimiter=","))
            Genre_Title.objects.bulk_create([
                Genre_Title(
                    id=row['id'],
                    title=Title.objects.get(pk=row['title_id']),
                    genre=Genre.objects.get(pk=row['genre_id'])
                )
                for row in data
            ])

    def handle(self, *args, **options):
        if options['clear']:
            Category.objects.all().delete()
            Title.objects.all().delete()
            Genre.objects.all().delete()
            Review.objects.all().delete()
            CustomUser.objects.exclude(pk=1).delete()

        self.categories_load()
        self.genres_load()
        self.users_load()
        self.titles_load()
        self.reviews_load()
        self.comments_load()
        self.genre_title_load()
