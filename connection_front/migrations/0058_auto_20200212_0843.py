# Generated by Django 2.2.9 on 2020-02-12 07:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('connection_front', '0057_auto_20200211_1546'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='messageprive',
            options={'ordering': ['-id'], 'verbose_name': 'message privé', 'verbose_name_plural': 'messages privé'},
        ),
    ]
