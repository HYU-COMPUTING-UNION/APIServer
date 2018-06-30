# Generated by Django 2.0.4 on 2018-04-27 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petitions', '0006_auto_20180427_2252'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['order'], 'verbose_name_plural': 'categories'},
        ),
        migrations.AlterField(
            model_name='category',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
    ]