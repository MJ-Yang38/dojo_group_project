# Generated by Django 2.2 on 2021-09-23 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('penfriends_app', '0007_auto_20210923_0122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='resident',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
