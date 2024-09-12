from django.shortcuts import render


# Create your views here.
def altprem_home(request):
    if request.method == 'POST' and 'run_script' in request.POST:
        # import function to run
        from .scraping import mainScrape
        
        # call function
        mainScrape() 

        # return user to required page
        return render(request, 'altprem/altprem_home.html', {})
    return render(request, 'altprem/altprem_home.html', {})