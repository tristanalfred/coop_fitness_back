# Generated by Django 2.2.1 on 2020-01-09 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connection_front', '0011_auto_20200109_1508'),
    ]

    operations = [
        migrations.AddField(
            model_name='utilisateur',
            name='image_profil',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
