# Generated by Django 2.2.9 on 2020-01-22 10:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('connection_front', '0020_auto_20200122_1137'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageGroupe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texte', models.CharField(max_length=300)),
                ('date_envoi', models.DateField()),
                ('expediteur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='connection_front.Utilisateur', verbose_name='expéditeur')),
                ('groupe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='connection_front.Groupe', verbose_name='groupe')),
            ],
            options={
                'verbose_name': 'message de groupe',
                'verbose_name_plural': 'messages de groupe',
            },
        ),
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_invitation', models.DateField()),
                ('texte', models.CharField(max_length=100, null=True)),
                ('destinataire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='connection_front.Utilisateur', verbose_name='destinataire')),
                ('groupe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='connection_front.Groupe', verbose_name='groupe')),
            ],
        ),
        migrations.CreateModel(
            name='DemandeInscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_invitation', models.DateField()),
                ('texte', models.CharField(max_length=100, null=True)),
                ('destinataire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='connection_front.Utilisateur', verbose_name='destinataire')),
                ('groupe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='connection_front.Groupe', verbose_name='groupe')),
            ],
            options={
                'verbose_name': "demande d'inscription",
                'verbose_name_plural': "demandes d'inscription",
            },
        ),
    ]