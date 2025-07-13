from django.shortcuts import render

# Create your views here.
def scrape_view(request):
    return render(request, 'scrape_view.html')