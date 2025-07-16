from django.shortcuts import render
from .forms import ScrapeForm
from .scraper_logic import run_scraper
from .models import ScrapeData

# Create your views here.
def scrape_view(request):
    if request.method == "POST": 
        input_form = ScrapeForm(request.POST)
        if input_form.is_valid():
            keyword = input_form.cleaned_data["keyword"]
            starting_point = input_form.cleaned_data["starting_point"]
            run_scraper(keyword, starting_point)
            result_data = ScrapeData.objects.all().order_by("distance")
            
            return render(request, 'scrape_view.html', {"form":input_form, 
                                                        "keyword":keyword, 
                                                        "starting_point": starting_point,
                                                        "results": result_data})
    else:
        input_form = ScrapeForm()
        
    result_data = ScrapeData.objects.all().order_by("distance")
    frist_record = ScrapeData.objects.first()
    keyword = frist_record.keyword if frist_record else "-"
    starting_point = frist_record.starting_point_given if frist_record else "-"
      
    return render(request, 'scrape_view.html', {"form":input_form, 
                                                "keyword": keyword,
                                                "starting_point": starting_point,
                                                "results": result_data})