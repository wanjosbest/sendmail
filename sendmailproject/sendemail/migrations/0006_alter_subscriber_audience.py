# Generated by Django 5.2.1 on 2025-07-07 17:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sendemail', '0005_alter_audience_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriber',
            name='audience',
            field=models.ForeignKey(default='mail', on_delete=django.db.models.deletion.CASCADE, related_name='subscribers', to='sendemail.audience'),
        ),
    ]
