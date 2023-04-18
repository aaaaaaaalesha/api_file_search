from django.db import models


class Search(models.Model):
    search_id = models.UUIDField(primary_key=True)
    text = models.CharField(max_length=255)
    file_mask = models.CharField(max_length=255)
    size_value = models.IntegerField()
    size_operator = models.CharField(max_length=2)
    creation_time_value = models.DateTimeField()
    creation_time_operator = models.CharField(max_length=2)


class SearchResult(models.Model):
    search = models.ForeignKey(Search, on_delete=models.CASCADE)
    path = models.CharField(max_length=255)
