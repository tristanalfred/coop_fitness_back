# Generated by Django 3.0.1 on 2020-01-08 10:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('connection_front', '0002_groupe_permission_utilisateur_ville'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Ville',
        ),
    ]
