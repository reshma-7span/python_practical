from django.urls import path
from .import views

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView
)

urlpatterns = [
    path('createuser', views.create_user, name='createuser'),
    path('createpost', views.create_post, name='createpost'),
    path('createlike', views.create_like, name='createlike'),
]