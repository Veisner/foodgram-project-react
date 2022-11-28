from rest_framework import status, viewsets
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from .filters import IngredientFilter, RecipeFilter
from .models import Ingredient, Recipe, Tag
from users.models import CustomUser
from .permissions import AdminOrReadOnly, AuthorOrAdminOrReadOnly, AuthorOrReadOnly
from .serializers import CustomUserSerializer, IngredientSerializer, RecipeListSerializer, RecipeEditSerializer, TagSerializer


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
        return RecipeListSerializer
    
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




class CustomUserViewSet(viewsets.ViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
