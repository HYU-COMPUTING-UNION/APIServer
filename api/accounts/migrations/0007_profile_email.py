# Generated by Django 2.0.4 on 2018-05-04 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20180419_1758'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.EmailField(default='test@example.com', max_length=254),
        ),
    ]