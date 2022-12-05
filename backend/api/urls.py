# from django.conf.urls import url
from django.urls import include, path, re_path

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from .views import (CustomUserViewSet, FavoriteViewSet, IngredientsViewSet, RecipesViewSet,
                    SubscribeView, ShoppingCartView, TagsViewSet)

router_v1 = DefaultRouter()
router_v1.register(r'users', CustomUserViewSet, basename='users')
router_v1.register(r'tags', TagsViewSet, basename='tags')
router_v1.register(r'ingredients', IngredientsViewSet, basename='ingredients')
router_v1.register(r'recipes', RecipesViewSet, basename='recipes')


urlpatterns = [
#    path('users/subscriptions/',
#         subscriptions, name='users_subs'),
    path('users/<int:user_id>/subscribe/',
         SubscribeView.as_view(), name='subscribe'),
    path('recipes/<int:recipe_id>/favorite/',
         FavoriteViewSet.as_view(), name='add_recipe_to_favorite'),
    path('recipes/<int:recipe_id>/shopping_cart/',
         ShoppingCartView.as_view(), name='add_recipe_to_shopping_cart'),
#    path('recipes/download_shopping_cart/',
#         DownloadPurchaseList.as_view(), name='dowload_shopping_cart'),
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]


schema_view = get_schema_view(
    openapi.Info(
        title='Foodgram API',
        default_version='v1/',
        description="Документация для проекта Foodgram",
        contact=openapi.Contact(email='admin@foodgram.ru'),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# urlpatterns += [
#     re_path(r'^swagger(?P<format>\.json|\.yaml)$',
#         schema_view.without_ui(cache_timeout=0), name='schema-json'),
#     re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
#         name='schema-swagger-ui'),
#     re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0),
#         name='schema-redoc'),
# ]
