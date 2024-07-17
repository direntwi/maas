from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DispatchViewSet

router = DefaultRouter()
router.register('dispatches', DispatchViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
