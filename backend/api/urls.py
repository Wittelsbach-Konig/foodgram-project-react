from django.urls import include, path
from rest_framework import routers

from .views.users_views import UserViewSet
from .views.recipes_views import (
    RecipeViewSet,
    TagViewSet,
    IngredientViewSet,
)


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
