# Generated by Django 5.1.1 on 2024-10-22 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partenaires', '0001_initial'),
        ('publications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='partenaires',
            field=models.ManyToManyField(blank=True, related_name='partenaires', to='partenaires.partenaire'),
        ),
    ]
