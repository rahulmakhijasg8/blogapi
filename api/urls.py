from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostsViewset,register,login

router = DefaultRouter()
router.register(r'posts', PostsViewset,basename='post')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
]