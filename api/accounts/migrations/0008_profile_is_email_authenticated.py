# Generated by Django 2.0.4 on 2018-05-04 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_profile_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_email_authenticated',
            field=models.BooleanField(default=False),
        ),
    ]