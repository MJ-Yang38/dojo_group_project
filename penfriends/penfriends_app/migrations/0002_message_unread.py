# Generated by Django 2.2 on 2021-09-18 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('penfriends_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='unread',
            field=models.BooleanField(default=True),
        ),
    ]