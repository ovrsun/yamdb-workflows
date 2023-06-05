from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import CustomUser

from api.validators import validate_year


class Category(models.Model):
    """Модель категорий к произведениям"""
    name = models.CharField(max_length=25,
                            verbose_name='Имя категории')
    slug = models.SlugField(unique=True,
                            verbose_name='Слаг категории')

    class Meta:
        ordering = ('id', )

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанров"""
    name = models.CharField(max_length=25,
                            verbose_name='Название жанра')
    slug = models.SlugField(unique=True,
                            verbose_name='Слаг жанра')

    class Meta:
        ordering = ('id', )

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведений"""
    name = models.CharField(max_length=256)
    category = models.ForeignKey(Category, related_name='titles',
                                 on_delete=models.SET_NULL, null=True,
                                 blank=True)
    genre = models.ManyToManyField(Genre, related_name='titles',
                                   verbose_name='Название жанра',
                                   through='Genre_Title')
    description = models.CharField(max_length=200, null=True, blank=True)
    year = models.IntegerField(validators=(validate_year,))

    class Meta:
        ordering = ('id', )

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель отзывов к произведениям"""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведения',
    )
    text = models.TextField(max_length=300)
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
    )
    score = models.IntegerField(
        verbose_name='Оценка отзыва',
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10),
        )
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ['id']
        constraints = [models.UniqueConstraint(fields=('title', 'author',),
                       name='unique_rewiew')]

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель для коменнтариев"""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )
    text = models.TextField(
        max_length=200,
        verbose_name='Текст комментария',
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ('id', )

    def __str__(self):
        return self.text


class Genre_Title(models.Model):
    title = models.ForeignKey(Title, null=False, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} <-> {self.genre}'
