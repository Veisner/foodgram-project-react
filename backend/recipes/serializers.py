import base64
from django.core.files.base import ContentFile
from django.db.models import F
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
# from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from .models import Ingredient, IngredientsAmount, Recipe, Tag, Favorite, TagsRecipe
from users.models import CustomUser, Follow


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')  
            ext = format.split('/')[-1]  
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)

class CustomUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(user=request.user, author=obj.id).exists()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientsAmountListSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientsAmount
        fields = ('id', 'name', 'amount', 'measurement_unit')


class IngredientsAmountCreateSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField(write_only=True)
    id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Ingredient
        fields = ('id', 'amount')


class RecipeListSerializer(serializers.ModelSerializer):
    image = Base64ImageField(
        required=False,
        allow_null=True
    )
    author = CustomUserSerializer(
        read_only=True
    )
    tags = TagSerializer(
        many=True,
        read_only=True
    )
    ingredients = IngredientsAmountListSerializer(
        source='recipe_ingredients',
        many=True, read_only=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time'
        )
    
    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Favorite.objects.filter(
            user=user,
            recipe=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(
            shopping_cart__user=user,
            id=obj.id
        ).exists()
    



#    def validate_ingredients(self, ingredients):
#        if not ingredients:
#            raise serializers.ValidationError(
#                'В рецепте не заполнены ингредиенты!')
#        return ingredients
#
#    def validate_tags(self, tags):
#        if not tags:
#            raise serializers.ValidationError('В рецепте не заполнены теги!')
#        return tags
#
#    def validate_image(self, image):
#        if not image:
#            raise serializers.ValidationError('Добавьте картинку рецепта!')
#        return image
#
#    def validate_name(self, name):
#        if not name:
#            raise serializers.ValidationError('Не заполнено название рецепта!')
#        return name
#
#    def validate_text(self, text):
#        if not text:
#            raise serializers.ValidationError('Не заполнено описание рецепта!')
#        return text
#
#    def validate_cooking_time(self, cooking_time):
#        if not cooking_time:
#            raise serializers.ValidationError(
#                'Не заполнено время приготовления рецепта!')
#        return cooking_time


class RecipeEditSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    ingredients = IngredientsAmountCreateSerializer(many=True)
    image = Base64ImageField(
        required=False,
        allow_null=True
    )

    class Meta:
        model = Recipe
        fields = ('ingredients', 'tags', 'image',
                  'name', 'text', 'cooking_time', 'author')

    def validate_ingredients(self, data):
        ingredients = self.initial_data.get('ingredients')
        if ingredients == []:
            raise serializers.ValidationError('Нужно выбрать ингридиенты')
        for ingredient in ingredients:
            if int(ingredient['amount']) <= 0:
                raise serializers.ValidationError('Выберите колличество')
        return data

    def get_ingredients(self, obj):
        ingredients = IngredientsAmount.objects.filter(recipe=obj)
        return IngredientsAmountListSerializer(ingredients).data

    def add_recipe_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            amount = ingredient['amount']
            if IngredientsAmount.objects.filter(
                recipe=recipe, ingredient=ingredient_id
            ).exists():
                amount += F('amount')
            IngredientsAmount.objects.update_or_create(
                recipe=recipe, ingredient=ingredient_id,
                defaults={'amount': amount})

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        for ingredient in ingredients:
            id = ingredient.get('id')
            amount = ingredient.get('amount')
            ingredient_id = get_object_or_404(Ingredient, id=id)
            IngredientsAmount.objects.create(
                recipe=recipe, ingredient=ingredient_id, amount=amount
            )
        recipe.save()
        return recipe

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        tags_list = validated_data.pop('tags')
        ingredients_list = validated_data.pop('ingredients')
        instance.tags.clear()
        instance.ingredients.clear()
        for tag in tags_list:
            tag_id = tag.id
            tag_object = get_object_or_404(Tag, id=tag_id)
            instance.tags.add(tag_object)
        for ingredient in ingredients_list:
            ingredient_id = ingredient.get('id')
            amount = ingredient.get('amount')
            ingredient_object = get_object_or_404(Ingredient, id=ingredient_id)
            instance.ingredients.add(
                ingredient_object,
                through_defaults={'amount': amount}
            )
        instance.save()
        return instance

    def to_representation(self, instance):
        serializer = RecipeListSerializer(
            instance,
            context=self.context
        )
        return serializer.data
