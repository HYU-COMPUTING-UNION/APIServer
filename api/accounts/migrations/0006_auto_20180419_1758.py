# Generated by Django 2.0.4 on 2018-04-19 08:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_profile_student_id'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Auth',
            new_name='AffiliationAuth',
        ),
    ]