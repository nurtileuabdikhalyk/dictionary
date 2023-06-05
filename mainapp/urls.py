from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='home'),
    path('search/', views.search, name='search'),
    path('word-single/<int:pk>', views.word_single, name='word_single'),
    path('favorites/', views.favorites, name='favorites'),

]
