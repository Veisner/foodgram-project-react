from django.urls import include, path, re_path

from rest_framework.routers import DefaultRouter

from recipes.views import (CustomUserViewSet, IngredientsViewSet,
                           RecipeViewSet, TagsViewSet)

router_v1 = DefaultRouter()
router_v1.register(r'users', CustomUserViewSet, basename='users')
router_v1.register(r'tags', TagsViewSet, basename='tags')
router_v1.register(r'ingredients', IngredientsViewSet, basename='ingredients')
router_v1.register(r'recipes', RecipeViewSet, basename='recipes')


urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
#    path('auth/', include('djoser.urls')),
#    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
