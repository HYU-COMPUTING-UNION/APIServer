# Generated by Django 2.0.4 on 2018-04-18 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auth',
            name='studentID',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]