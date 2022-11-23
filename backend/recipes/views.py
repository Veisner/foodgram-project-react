from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .filters import IngredientFilter, RecipeFilter
from .models import Ingredient, Recipe, Tag
from users.models import CustomUser
from .permissions import AdminOrReadOnly, AuthorOrAdminOrReadOnly
from .serializers import CustomUserSerializer, IngredientSerializer, RecipeSerializer, TagSerializer


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
    permission_classes = (AuthorOrAdminOrReadOnly,)
    queryset = Recipe.objects.select_related('author')
    serializer_class = RecipeSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    http_method_names = ('get', 'post', 'put', 'patch', 'delete',)


class CustomUserViewSet(viewsets.ViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
