# Generated by Django 3.0.5 on 2020-05-12 09:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Users',
            new_name='Account',
        ),
    ]
