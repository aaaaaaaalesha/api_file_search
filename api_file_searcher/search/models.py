from django.db import models


class Search(models.Model):
    class Operators(models.TextChoices):
        EQ = 'eq'
        GR = 'gt'
        LT = 'lt'
        GE = 'ge'
        LE = 'le'

    search_id = models.UUIDField(
        primary_key=True,
    )
    text = models.CharField(
        max_length=255,
        null=True,
    )
    file_mask = models.CharField(
        max_length=255,
        null=True,
    )
    # Size.
    size_value = models.PositiveIntegerField(
        null=True,
    )
    size_operator = models.CharField(
        max_length=2,
        null=True,
        choices=Operators.choices,
    )
    # Creation time.
    creation_time_value = models.DateTimeField(
        null=True,
    )
    creation_time_operator = models.CharField(
        max_length=2,
        null=True,
        choices=Operators.choices,
    )
    paths = models.TextField(
        default='[]',
    )
