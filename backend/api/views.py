from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import Subscribe, User

from .filters import IngredientFilter, RecipeFilter
from .mixins import RetrieveListViewSet
from .paginators import NewPageNumberPaginator
from .permissions import IsAuthorAdminOrReadOnly
from .serializers import (CustomUserSerializer, FavoriteSerializer,
                          IngredientSerializer, PasswordSerializer,
                          RecipeCreateSerializer, RecipeListSerializer,
                          ShoppingCartSerializer, SubscribersSerializer,
                          SubscribeSerializer, TagSerializer)


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

    @action(detail=False,
            methods=['post'],
            permission_classes=(IsAuthenticated, ))
    def set_password(self, request, pk=None):
        user = self.request.user
        serializer = PasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.data['new_password'])
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagsViewSet(RetrieveListViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny, )
    pagination_class = None


class IngredientsViewSet(RetrieveListViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny, )
    filter_backends = (DjangoFilterBackend, )
    filterset_class = IngredientFilter
    pagination_class = None


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeListSerializer
    permission_classes = (IsAuthorAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipeFilter
    pagination_class = NewPageNumberPaginator

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeListSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save()


@api_view(['get'])
def subscriptions(request):
    user_obj = User.objects.filter(following__user=request.user)
    paginator = PageNumberPagination()
    paginator.page_size = 10
    result_page = paginator.paginate_queryset(user_obj, request)
    serializer = SubscribersSerializer(
        result_page,
        many=True,
        context={'current_user': request.user}
    )
    return paginator.get_paginated_response(serializer.data)


class SubscribeView(APIView):

    def post(self, request, user_id):
        user = request.user
        data = {
            'user': user.id,
            'author': user_id
        }
        serializer = SubscribeSerializer(
            data=data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

    def delete(self, request, user_id):
        user = request.user
        follow = get_object_or_404(
            Subscribe,
            user=user,
            author_id=user_id
        )
        follow.delete()
        return Response('Вы отписались', status.HTTP_204_NO_CONTENT)


class FavoriteViewSet(APIView):
    permission_classes = (IsAuthorAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipeFilter

    def post(self, request, recipe_id):
        user = request.user.id
        data = {
            'user': user,
            'recipe': recipe_id
        }
        serializer = FavoriteSerializer(
            data=data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        user = request.user
        favorite_recipe = get_object_or_404(
            Favorite,
            user=user,
            recipe__id=recipe_id
        )
        favorite_recipe.delete()
        return Response(
            'Рецепт удален',
            status.HTTP_204_NO_CONTENT
        )


class ShoppingCartView(APIView):

    def post(self, request, recipe_id):
        user = request.user.id
        data = {
            'user': user,
            'recipe': recipe_id
        }
        serializer = ShoppingCartSerializer(
            data=data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        user = request.user
        purchace_list_recipe = get_object_or_404(
            ShoppingCart,
            user=user,
            recipe__id=recipe_id
        )
        purchace_list_recipe.delete()
        return Response(
            'Рецепт удален',
            status.HTTP_204_NO_CONTENT
        )


class DownloadShoppingCart(APIView):

    def get(self, request):
        shopping_cart = request.user.shopping_cart.all()
        shopping_list = {}
        for purchase in shopping_cart:
            ingredients = purchase.recipe.ingredient_recipe.all()
            for ingredient in ingredients:
                name = ingredient.ingredient.name
                amount = ingredient.amount
                unit = ingredient.ingredient.measurement_unit
                if name not in shopping_list:
                    shopping_list[name] = {
                        'amount': amount,
                        'unit': unit
                    }
                else:
                    shopping_list[name]['amount'] = (shopping_list[name]
                                                     ['amount'] + amount)
        shoplist = []
        for item in shopping_list:
            shoplist.append(f'{item} ({shopping_list[item]["unit"]}) — '
                            f'{shopping_list[item]["amount"]} \n')
        response = HttpResponse(shoplist, 'Content-Type: application/pdf')
        response['Content-Disposition'] = 'attachment; filename="shoplist.pdf"'
        return response
