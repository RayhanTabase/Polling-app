# Generated by Django 3.2.3 on 2021-06-13 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0016_auto_20210609_2038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='country_code',
            field=models.CharField(blank=True, default='233', max_length=30),
        ),
        migrations.AlterField(
            model_name='user',
            name='other_names',
            field=models.CharField(blank=True, default=' ', max_length=50, null=True),
        ),
    ]
