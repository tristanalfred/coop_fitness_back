# Generated by Django 2.2.9 on 2020-02-03 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connection_front', '0033_auto_20200203_0945'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='utilisateur',
            options={'verbose_name': 'utilisateur', 'verbose_name_plural': 'utilisateurs'},
        ),
        migrations.AddField(
            model_name='demandeinscription',
            name='accepte',
            field=models.BooleanField(null=True),
        ),
    ]
