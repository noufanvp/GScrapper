from django.shortcuts import render
from .forms import ScrapeForm

# Create your views here.
def scrape_view(request):
    if request.method == "POST": 
        input_form = ScrapeForm(request.POST)
        if input_form.is_valid():
            keyword = input_form.cleaned_data["keyword"]
            starting_point = input_form.cleaned_data["starting_point"]
            result_data = run_scraper(keyword, starting_point)
    else:
        input_form = ScrapeForm()
    return render(request, 'scrape_view.html', {"form":input_form})