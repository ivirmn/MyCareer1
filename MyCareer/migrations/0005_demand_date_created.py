# Generated by Django 4.1.9 on 2023-06-26 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyCareer', '0004_alter_demand_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='demand',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
