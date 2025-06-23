from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('retrieve/', views.retrieve, name='retrieve'),
    path('paste/<str:code>/', views.display_paste, name='display_paste'),
    path('paste/<str:code>/download/', views.download_file, name='download_file'),
    path('api/create/', views.api_create, name='api_create'),
]
