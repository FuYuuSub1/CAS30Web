# Generated by Django 3.0.4 on 2020-03-15 13:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookinstance',
            old_name='imprint',
            new_name='member',
        ),
    ]
