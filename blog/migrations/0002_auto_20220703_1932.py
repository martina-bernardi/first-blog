# Generated by Django 3.2.13 on 2022-07-03 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='hash',
            field=models.CharField(default=None, max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='txId',
            field=models.CharField(default=None, max_length=66, null=True),
        ),
    ]
