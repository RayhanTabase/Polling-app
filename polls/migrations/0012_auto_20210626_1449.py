# Generated by Django 3.2.3 on 2021-06-26 14:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0011_auto_20210626_1445'),
    ]

    operations = [
        migrations.CreateModel(
            name='PollCategoryGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='polls.poll')),
            ],
        ),
        migrations.AddField(
            model_name='pollcategory',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='polls.pollcategorygroup'),
        ),
    ]
