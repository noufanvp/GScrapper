from django.db import models

# Create your models here.
class ScrapeData(models.Model):
    keyword = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255)
    rating = models.CharField(max_length=10)
    review_count = models.CharField(max_length=10)
    category = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    status = models.CharField(max_length=50)
    starting_point_given = models.CharField(max_length=255, null=True)
    starting_point = models.CharField(max_length=255)
    distance = models.FloatField()
    time_req = models.CharField(max_length=50)
    location_url = models.URLField()
