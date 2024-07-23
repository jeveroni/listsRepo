from django.shortcuts import render
from .models import List

# Create your views here.
def list_list(request):
    lists = List.objects.all()
    return render(request, 'listApp/list_list.html', {'lists': lists})