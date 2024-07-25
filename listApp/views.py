from django.shortcuts import render, get_object_or_404
from .models import List, Item

# Create your views here.
def list_list(request):
    lists = List.objects.all()
    return render(request, 'listApp/list_list.html', {'lists': lists})

def list_detail( request, pk):
    list = get_object_or_404( List, pk=pk)
    items = Item.objects.filter( list_id = pk )
    return render(request, 'listApp/list_detail.html', {'list': list, 'items': items})