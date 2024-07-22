from django.shortcuts import render

# Create your views here.
def list_list(request):
    return render(request, 'listApp/list_list.html', {})