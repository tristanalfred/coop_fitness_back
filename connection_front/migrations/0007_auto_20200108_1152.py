# Generated by Django 3.0.1 on 2020-01-08 10:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('connection_front', '0006_demandeinscription_invitation_messagegroupe_messageprive_suivi'),
    ]

    operations = [
        migrations.RenameField(
            model_name='suivi',
            old_name='concernte',
            new_name='concerne',
        ),
    ]
