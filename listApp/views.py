from django.shortcuts import render, get_object_or_404
from .models import List, Item
from.forms import ItemForm
from django.utils import timezone
from django.shortcuts import redirect

# Create your views here.
def list_list(request):
    lists = List.objects.all()
    return render(request, 'listApp/list_list.html', {'lists': lists })

def list_detail( request, pk):
    list = get_object_or_404( List, pk=pk)
    items = Item.objects.filter( list_id = pk )
    return render(request, 'listApp/list_detail.html', {'list': list, 'items': items})

def item_new( request ):
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_date = timezone.now()
            item.save()
            return redirect('list_detail', pk = item.list.id)   
    else:
        form = ItemForm()
    return render(request, 'listApp/item_edit.html', {'form': form})

def item_edit(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == "POST":
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()
            return redirect('list_detail', pk=item.list.pk)
    else:
        form = ItemForm(instance=item)
    return render(request, 'listApp/item_edit.html', {'form': form})