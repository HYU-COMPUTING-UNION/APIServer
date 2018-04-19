# Generated by Django 2.0.4 on 2018-04-19 17:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0006_auto_20180419_1758'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sub_categories', to='petitions.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Petition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('issued_at', models.DateField(auto_now_add=True)),
                ('expired_at', models.DateField()),
                ('answered_at', models.DateField(blank=True, null=True)),
                ('is_in_progress', models.BooleanField(default=False)),
                ('assentients', models.ManyToManyField(related_name='assentient_petitions', to='accounts.Profile')),
                ('categories', models.ManyToManyField(related_name='petitions', to='petitions.Category')),
                ('issuer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issued_petitions', to='accounts.Profile')),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='petition',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='answer', to='petitions.Petition'),
        ),
    ]
