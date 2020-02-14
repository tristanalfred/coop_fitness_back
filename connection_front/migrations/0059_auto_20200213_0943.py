# Generated by Django 2.2.9 on 2020-02-13 08:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('connection_front', '0058_auto_20200212_0843'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='messagegroupe',
            options={'ordering': ['-id'], 'verbose_name': 'message de groupe', 'verbose_name_plural': 'messages de groupe'},
        ),
        migrations.AlterField(
            model_name='suivi',
            name='concerne',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='connection_front.Utilisateur', verbose_name='concerne'),
        ),
    ]
