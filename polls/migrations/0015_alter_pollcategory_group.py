# Generated by Django 3.2.3 on 2021-06-26 21:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0014_auto_20210626_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pollcategory',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='categories', to='polls.pollcategorygroup'),
        ),
    ]
