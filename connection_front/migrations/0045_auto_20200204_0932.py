# Generated by Django 2.2.9 on 2020-02-04 08:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('connection_front', '0044_remove_membregroupe_membre'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groupe',
            name='membres',
        ),
        migrations.DeleteModel(
            name='MembreGroupe',
        ),
    ]
