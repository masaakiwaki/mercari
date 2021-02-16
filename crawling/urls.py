from django.urls import path
from . import views

urlpatterns = [
    path('', views.Scraping, name='index'),
    path('find/', views.Scraping_Find, name='find'),
    path('download_list/', views.Download_List, name='download_list'),
]
