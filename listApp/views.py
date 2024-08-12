from django.shortcuts import render, get_object_or_404
from .models import List, Item
from.forms import ItemForm
from django.utils import timezone
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
import json


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

@require_http_methods(["PUT"])
def update_item(request):
    try:
        data = json.loads(request.body)  # Parse the JSON data from the request body
        item_id = data.get('id')  # Extract the item ID
        is_completed = data.get('checked')  # Extract the new checkbox state
        
        # Fetch the corresponding Task object
        item = Item.objects.get(id=item_id)
        item.completed = is_completed  # Update the 'completed' field
        item.save()  # Save the changes to the database
        
        return JsonResponse({'status': 'success', 'id': item_id, 'completed': is_completed})
    except Item.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Item not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)






def test_page( request ):
    items = Item.objects.all()
    if request.method == 'POST':
        checkbox_value = request.POST.get('myCheckbox')
        if checkbox_value == 'checked':
            # Handle the checkbox being checked
            return HttpResponse('Checkbox was checked!')
        else:
            # Handle the checkbox being unchecked or not submitted
            return HttpResponse('Checkbox was not checked!')
    return render(request, 'listApp/test_page.html', {'items': items})

