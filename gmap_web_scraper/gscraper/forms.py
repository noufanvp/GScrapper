from django import forms

class ScrapeForm(forms.Form):
    keyword = forms.CharField(label="Search Keyword", max_length=255)
    starting_point = forms.CharField(label="Starting location", max_length=255)