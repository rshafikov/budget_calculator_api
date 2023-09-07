from django.urls import include, path
from rest_framework import routers

from .views import CategoryViewSet, RecordViewSet

router = routers.DefaultRouter()
router.register('records', RecordViewSet, basename='records')
router.register('categories', CategoryViewSet, basename='categories')


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
