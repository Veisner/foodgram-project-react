from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            ShoppingCart, Tag)
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Subscribe, User

from .filters import IngredientFilter, RecipeFilter
from .mixins import RetrieveListViewSet
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
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = PasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            user.set_password(serializer.data['new_password'])
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False,
            methods=['get'],
            permission_classes=(IsAuthenticated, ))
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(follower__user=user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(
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
        author = get_object_or_404(User, id=id)
        subscribe = Subscribe.objects.filter(user=user, author=author)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if request.method == 'GET':
            if subscribe.exists():
                data = {
                    'errors': ('Вы уже подписаны.')}
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            Subscribe.objects.create(user=user, author=author)
            serializer = SubscribeSerializer(
                author,
                context={'request': request}
            )
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            if not subscribe.exists():
                data = {'errors': 'Вы не подписаны.'}
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            subscribe.delete()
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

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeListSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save()

    # @action(
    #     methods=['get', 'delete'],
    #     detail=True,
    #     permission_classes=(IsAuthenticated, )
    # )
    # def favorite(self, request, pk=None):
    #     user = self.request.user
    #     recipe = get_object_or_404(Recipe, pk=pk)
    #     in_favorite = Favorite.objects.filter(
    #         user=user, recipe=recipe
    #     )
    #     if user.is_anonymous:
    #         return Response(status=status.HTTP_401_UNAUTHORIZED)
    #     if request.method == 'GET':
    #         if not in_favorite:
    #             favorite = Favorite.objects.create(user=user, recipe=recipe)
    #             serializer = FavoriteSerializer(favorite.recipe)
    #             return Response(
    #                 data=serializer.data,
    #                 status=status.HTTP_201_CREATED
    #             )
    #     elif request.method == 'DELETE':
    #         if not in_favorite:
    #             data = {'errors': 'Нет такого рецепта.'}
    #             return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    #         in_favorite.delete()
    #         return Response(status=status.HTTP_204_NO_CONTENT)

    # @action(
    #     detail=True,
    #     methods=["get", "delete"],
    #     permission_classes=[IsAuthenticated, ],
    # )
    # def shopping_cart(self, request, pk=None):
    #     user = self.request.user
    #     recipe = get_object_or_404(Recipe, pk=pk)
    #     in_shopping_cart = ShoppingCart.objects.filter(
    #         user=user,
    #         recipe=recipe
    #     )
    #     if user.is_anonymous:
    #         return Response(status=status.HTTP_401_UNAUTHORIZED)
    #     if request.method == 'GET':
    #         if not in_shopping_cart:
    #             shopping_cart = ShoppingCart.objects.create(
    #                 user=user,
    #                 recipe=recipe
    #             )
    #             serializer = ShoppingCartSerializer(shopping_cart.recipe)
    #             return Response(
    #                 data=serializer.data,
    #                 status=status.HTTP_201_CREATED
    #             )
    #     elif request.method == 'DELETE':
    #         if not in_shopping_cart:
    #             data = {'errors': 'Нет такого рецепта.'}
    #             return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    #         in_shopping_cart.delete()
    #         return Response(status=status.HTTP_204_NO_CONTENT)

#    @action(
#        methods=['get'],
#        detail=False,
#        permission_classes=[IsAuthenticated, ],
#    )
#    def download_shopping_cart(self, request):

# @api_view(['get'])
# def subscriptions(request):
#     user_obj = User.objects.filter(following__user=request.user)
#     paginator = PageNumberPagination()
#     paginator.page_size = 10
#     result_page = paginator.paginate_queryset(user_obj, request)
#     serializer = SubscribeSerializer(
#         result_page,
#         many=True,
#         context={'current_user': request.user}
#     )
#     return paginator.get_paginated_response(serializer.data)

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
