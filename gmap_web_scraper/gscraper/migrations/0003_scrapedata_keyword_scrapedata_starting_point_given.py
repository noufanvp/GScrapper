# Generated by Django 5.2.4 on 2025-07-16 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gscraper', '0002_rename_locaction_url_scrapedata_location_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='scrapedata',
            name='keyword',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='scrapedata',
            name='starting_point_given',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
