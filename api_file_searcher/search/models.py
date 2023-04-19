from django.db import models


class Search(models.Model):
    search_id = models.UUIDField(
        primary_key=True,
    )
    paths = models.TextField(
        default='[]',
    )
