# Generated by Django 4.2.3 on 2023-07-18 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('piano_app', '0002_piano_vote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='piano',
            name='vote',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
