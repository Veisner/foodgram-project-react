from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        unique=True,
        max_length=50,
        verbose_name='Название тэга'
    )
    color = models.CharField(
        max_length=7,
        default="#ffffff",
        verbose_name='Цветовой HEX-код'
    )
    slug = models.SlugField(
        unique=True,
        max_length=200,
        verbose_name='Слаг тэга'
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        null=False,
        verbose_name='Название'
    )
    measurement_unit = models.CharField(
        max_length=20,
        null=False,
        verbose_name='Единицы измерения'
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        ordering = ('name',)
        
    def __str__(self):
        return self.name

class Recipe(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта',
        related_name='recipes'
    )
    image = models.ImageField(
        blank=True,
        upload_to='recipes/images/',
        verbose_name='Изображение'
    )
    text = models.TextField(
        max_length=1000,
        verbose_name='Описание рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientCount',
        related_name='recipes',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэг',
        related_name='recipes'
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(
            1, message='Минимальное время приготовления 1 минута.'
            )
        ),
        verbose_name='Время приготовления'
    )



    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f'{self.title[:20]}, {self.author.username}'

# class IngredientCount(models.Model):
