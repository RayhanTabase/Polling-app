# Generated by Django 3.2.3 on 2021-07-12 11:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polls', '0031_auto_20210712_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restrictionkey',
            name='usedBy',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='vote',
            name='voter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='voted_polls', to=settings.AUTH_USER_MODEL),
        ),
    ]
