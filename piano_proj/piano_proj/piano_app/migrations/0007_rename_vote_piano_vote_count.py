# Generated by Django 5.0.7 on 2024-10-30 18:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('piano_app', '0006_alter_piano_vote'),
    ]

    operations = [
        migrations.RenameField(
            model_name='piano',
            old_name='vote',
            new_name='vote_count',
        ),
    ]
