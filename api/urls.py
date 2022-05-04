from django.urls import include, path
from rest_framework import routers

from .views import RecordViewSet, UserViewSet

router = routers.DefaultRouter()
router.register('records', RecordViewSet)
router.register('users', UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
]