# Generated by Django 4.2 on 2023-04-19 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0002_search_paths_alter_search_creation_time_operator_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='search',
            name='creation_time_value',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
