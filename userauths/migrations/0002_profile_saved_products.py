# Generated by Django 5.0 on 2024-09-29 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('userauths', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='saved_products',
            field=models.ManyToManyField(blank=True, related_name='saved_by', to='core.product'),
        ),
    ]
