from django.urls import path
from .import views



urlpatterns = [
    path('createuser', views.create_user, name='createuser'),
    path('createpost', views.create_post, name='createpost'),
    path('createlike', views.create_like, name='createlike'),
    path('getuser/<int:user_id>', views.get_user, name='getuser'),
    path('getpost/<int:post_id>', views.get_post, name='getpost'),
    path('getlike/<int:like_id>', views.get_like, name='getlike'),
    path('updateuser/<int:user_id>', views.update_user, name='updateuser'),
    path('updatepost/<int:post_id>', views.update_post, name='updatepost'),
    path('updatelike/<int:like_id>', views.update_like, name='updatelike'),
    path('deleteuser/<int:user_id>', views.delete_user, name='deleteuser'),
    path('deletepost/<int:post_id>', views.delete_post, name='deletepost'),
    path('deletelike/<int:like_id>', views.delete_like, name='deletelike'),
    path('getallpost', views.get_all_posts, name='getallpost'),
]