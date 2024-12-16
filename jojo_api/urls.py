from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('characters/', views.list_characters, name='list_characters'),
    path('fetch-data/', views.fetch_and_store_jojo_data, name='fetch_and_store_jojo_data'),
    path('theories/', views.list_theories, name='list_theories'),
    path('like-character/<int:character_id>/', views.like_character, name='like_character'),
    path('like-theory/<int:theory_id>/', views.like_theory, name='like_theory'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]