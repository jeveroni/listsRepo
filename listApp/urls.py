from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views


urlpatterns = [
    path('', views.list_list, name='list_list'),
    path('list/<int:pk>/', views.list_detail, name='list_detail'),
    path('list/new/', views.list_new, name='list_new'),
    path('list/<int:pk>/item_new', views.item_new, name='item_new'),
    path('item/<int:pk>/edit', views.item_edit, name='item_edit'),
    path('test/', views.test_page, name = 'test_page'),
    path('update-item/', csrf_exempt(views.update_item), name='update_item'),
]