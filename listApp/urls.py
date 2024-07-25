from django.urls import path
from . import views


urlpatterns = [
    path('', views.list_list, name='list_list'),
    path('list/<int:pk>/', views.list_detail, name='list_detail'),
]