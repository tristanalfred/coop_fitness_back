# Generated by Django 2.2.9 on 2020-01-22 15:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('connection_front', '0027_auto_20200122_1540'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='demandeinscription',
            unique_together={('expediteur', 'groupe')},
        ),
    ]
