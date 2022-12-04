import csv

from django.db.models import Sum
from rest_framework.decorators import action
from rest_framework import status, viewsets
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from .filters import IngredientFilter, RecipeFilter
from .models import Ingredient, Recipe, Tag, Favorite, ShoppingCart, IngredientsAmount
from users.models import CustomUser, Follow
from .permissions import AdminOrReadOnly, AuthorOrAdminOrReadOnly, AuthorOrReadOnly
from .serializers import (CustomUserSerializer, IngredientSerializer, RecipeListSerializer,
                         RecipeEditSerializer, TagSerializer, FavoriteSerializer, ShoppingCartSerializer,
                         FollowSerializer)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (AdminOrReadOnly,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    http_method_names = ('get',)


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (AdminOrReadOnly,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    http_method_names = ('get',)


class RecipeViewSet(viewsets.ModelViewSet):
    permission_classes = (AuthorOrReadOnly,)
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeListSerializer
        return RecipeEditSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer = RecipeListSerializer(
            instance=serializer.instance,
            context={'request': self.request}
        )
        return Response(
            serializer.data, status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        serializer = RecipeListSerializer(
            instance=serializer.instance,
            context={'request': self.request},
        )
        return Response(
            serializer.data, status=status.HTTP_200_OK
        )

    def add_recipe(self, request, model, pk=None):
        user = request.user
        if model.objects.filter(user=user, recipe__id=pk).exists():
            return Response({
                'errors': 'Такой рецепт уже есть.'
            }, status=status.HTTP_400_BAD_REQUEST
            )
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = RecipeListSerializer(recipe, fields='__all__')
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def del_recipe(self, request, model, pk=None):
        user = request.user
        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({
            'errors': 'Такого рецепта нет.'
        }, status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['get', 'delete'],
        detail=True,
        permission_classes=(IsAuthenticated, )
    )
    def favorite(self, request, pk=None):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        in_favorite = Favorite.objects.filter(
            user=user, recipe=recipe
        )
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if request.method == 'GET':
            if not in_favorite:
                favorite = Favorite.objects.create(user=user, recipe=recipe)
                serializer = FavoriteSerializer(favorite.recipe)
                return Response(
                    data=serializer.data,
                    status=status.HTTP_201_CREATED
                )
        elif request.method == 'DELETE':
            if not in_favorite:
                data = {'errors': 'Нет такого рецепта.'}
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            in_favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=["get", "delete"],
        permission_classes=[IsAuthenticated, ],
    )
    def shopping_cart(self, request, pk=None):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        in_shopping_cart = ShoppingCart.objects.filter(
            user=user,
            recipe=recipe
        )
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if request.method == 'GET':
            if not in_shopping_cart:
                shopping_cart = ShoppingCart.objects.create(
                    user=user,
                    recipe=recipe
                )
                serializer = ShoppingCartSerializer(shopping_cart.recipe)
                return Response(
                    data=serializer.data,
                    status=status.HTTP_201_CREATED
                )
        elif request.method == 'DELETE':
            if not in_shopping_cart:
                data = {'errors': 'Нет такого рецепта.'}
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            in_shopping_cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['get'],
        detail=False,
        permission_classes=[IsAuthenticated, ],
    )
    def download_shopping_cart(self, request):
        user = self.request.user
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        ingredients = IngredientsAmount.objects.filter(
            recipe__shopping_cart__user=request.user
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(ingredient_amount=Sum('amount')).values_list(
            'ingredient__name', 'ingredient__measurement_unit',
            'ingredient_amount')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = ('attachment;'
                                           'filename="Shoppingcart.csv"')
        response.write(u'\ufeff'.encode('utf8'))
        writer = csv.writer(response)
        for item in list(ingredients):
            writer.writerow(item)
        return response




class CustomUserViewSet(viewsets.ViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    @action(detail=False,
            methods=['get'],
            permission_classes=(IsAuthenticated, ))
    def subscriptions(self, request):
        user = request.user
        queryset = CustomUser.objects.filter(follower__user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        methods=['get', 'delete'],
        detail=True,
        permission_classes=(IsAuthenticated, )
    )
    def subscribe(self, request, id):
        user = self.request.user
        author = get_object_or_404(CustomUser, id=id)
        subscribe = Follow.objects.filter(user=user, author=author)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if request.method == 'GET':
            if subscribe.exists():
                data = {
                    'errors': ('Вы уже подписаны на этого автора.')}
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            Follow.objects.create(user=user, author=author)
            serializer = FollowSerializer(
                author,
                context={'request': request}
            )
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            if not subscribe.exists():
                data = {'errors': 'Вы не подписаны на этого автора.'}
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            subscribe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteApiView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, favorite_id):
        user = request.user
        data = {
            'recipe': favorite_id,
            'user': user.id
        }
        serializer = FavoriteSerializer(data=data,
                                        context={'request': request})
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, favorite_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=favorite_id)
        Favorite.objects.filter(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartApiView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, recipe_id):
        user = request.user
        data = {
            'recipe': recipe_id,
            'user': user.id
        }
        context = {'request': request}
        serializer = ShoppingCartSerializer(data=data,
                                            context=context)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        ShoppingCart.objects.filter(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
