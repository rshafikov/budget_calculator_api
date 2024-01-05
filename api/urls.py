from django.urls import include, path
from rest_framework import routers

from .views import CategoryViewSet, RecordViewSet, UserViewSet

router = routers.DefaultRouter()
router.register('records', RecordViewSet, basename='records')
router.register('categories', CategoryViewSet, basename='categories')
router.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
