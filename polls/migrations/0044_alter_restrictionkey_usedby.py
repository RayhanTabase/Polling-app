# Generated by Django 3.2.3 on 2021-07-28 13:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polls', '0043_alter_candidate_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restrictionkey',
            name='usedBy',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='specialKey', to=settings.AUTH_USER_MODEL),
        ),
    ]
