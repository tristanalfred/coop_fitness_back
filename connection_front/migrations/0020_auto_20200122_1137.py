# Generated by Django 2.2.9 on 2020-01-22 10:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('connection_front', '0019_groupe'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invitation',
            name='destinataire',
        ),
        migrations.RemoveField(
            model_name='messagegroupe',
            name='expediteur',
        ),
        migrations.DeleteModel(
            name='DemandeInscription',
        ),
        migrations.DeleteModel(
            name='Invitation',
        ),
        migrations.DeleteModel(
            name='MessageGroupe',
        ),
    ]