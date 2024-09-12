from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views


urlpatterns = [
    path('altprem/', views.altprem_home, name='altprem_home'),
]