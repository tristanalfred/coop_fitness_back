# Generated by Django 2.2.1 on 2020-01-09 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connection_front', '0009_auto_20200108_1523'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='demandeinscription',
            options={'verbose_name': "demande d'inscription", 'verbose_name_plural': "demandes d'inscription"},
        ),
        migrations.AlterModelOptions(
            name='messagegroupe',
            options={'verbose_name': 'message de groupe', 'verbose_name_plural': 'messages de groupe'},
        ),
        migrations.AlterModelOptions(
            name='messageprive',
            options={'verbose_name': 'message privé', 'verbose_name_plural': 'messages privé'},
        ),
        migrations.AddField(
            model_name='ville',
            name='option',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]