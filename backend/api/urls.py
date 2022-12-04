from django.urls import include, path, re_path

from rest_framework.routers import DefaultRouter

from recipes.views import (CustomUserViewSet, IngredientsViewSet,
                           RecipeViewSet, TagsViewSet, ShoppingCartApiView, FavoriteApiView)

router_v1 = DefaultRouter()
router_v1.register(r'users', CustomUserViewSet, basename='users')
router_v1.register(r'tags', TagsViewSet, basename='tags')
router_v1.register(r'ingredients', IngredientsViewSet, basename='ingredients')
router_v1.register(r'recipes', RecipeViewSet, basename='recipes')


urlpatterns = [
#    path('recipes/download_shopping_cart/', DownloadShoppingCart.as_view()),
    path('', include(router_v1.urls)),
#    path('recipes/<int:favorite_id>/favorite/', FavoriteApiView.as_view()),
#    path('recipes/<int:recipe_id>/shopping_cart/', ShoppingCartApiView.as_view()),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
