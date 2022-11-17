from django.core.validators import MinValueValidator
from django.db import models

from users.models import CustomUser


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
        CustomUser,
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
        through='IngredientsAmount',
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
            1, message='Время приготовления не может быть меньше 1 минуты'
            )
        ),
        verbose_name='Время приготовления'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name


class IngredientsAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name='Ингредиенты'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='count_ingredient',
        verbose_name='Рецепт'
    )
    amount = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(
            1, message='Минимум 1 ингридиент'
            )
        ),
        default=1,
        verbose_name='Количество ингридиентов'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique_ingredient',
            )
        ]
        verbose_name = 'Ингредиента в рецепте'
        verbose_name_plural = 'Ингредиентов в рецептах'
        ordering = ('recipe',)

    def __str__(self):
        return f'{self.amount} {self.ingredient}'


class Favorite(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='favorites',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='favorites'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite',
            )
        ]
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        ordering = ('user', 'recipe',)
    
    def __str__(self):
        return f'Рецепт {self.recipe} в избранном у {self.user}'
