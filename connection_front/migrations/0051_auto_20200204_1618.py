# Generated by Django 2.2.9 on 2020-02-04 15:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('connection_front', '0050_remove_groupe_createur'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='membregroupe',
            unique_together={('membre', 'groupe')},
        ),
    ]
