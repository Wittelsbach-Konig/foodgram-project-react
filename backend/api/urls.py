from django.urls import include, path
from rest_framework import routers

from api.views.recipes_views import (IngredientViewSet,
                                     RecipeViewSet,
                                     TagViewSet)
from api.views.users_views import UserViewSet

API_PREFIX = 'v1/'

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
