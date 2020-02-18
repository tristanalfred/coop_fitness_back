# Generated by Django 2.2.9 on 2020-02-04 08:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('connection_front', '0036_remove_groupe_membres'),
    ]

    operations = [
        migrations.CreateModel(
            name='MembreGroupe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createur', models.BooleanField(default=False)),
                ('responsable', models.BooleanField(default=False)),
                ('groupe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='connection_front.Groupe', verbose_name='groupe')),
                ('membre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='connection_front.Utilisateur', verbose_name='membre')),
            ],
        ),
    ]