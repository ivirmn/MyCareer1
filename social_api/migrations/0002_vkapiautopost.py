# Generated by Django 4.1.9 on 2024-04-24 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VkApiAutopost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('VkTokenAutopost', models.CharField(blank=True, max_length=200)),
                ('VkGroupId', models.CharField(blank=True, max_length=200)),
            ],
        ),
    ]
