from django.urls import path
from djoser.views import UserViewSet

urlpatterns = [
    path('activate/', UserViewSet.as_view({'get': 'activation', 'post': 'activation'}), name='user-activation'),
]
