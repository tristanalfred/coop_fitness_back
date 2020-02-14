# Generated by Django 2.2.9 on 2020-02-10 10:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('connection_front', '0051_auto_20200204_1618'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='demandeinscription',
            options={'ordering': ['-id'], 'verbose_name': "demande d'inscription", 'verbose_name_plural': "demandes d'inscription"},
        ),
        migrations.AlterModelOptions(
            name='invitation',
            options={'ordering': ['-id']},
        ),
        migrations.AlterField(
            model_name='membregroupe',
            name='groupe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='connection_front.Groupe', verbose_name='groupe'),
        ),
    ]
