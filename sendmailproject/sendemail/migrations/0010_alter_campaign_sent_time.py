# Generated by Django 5.2.1 on 2025-07-10 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sendemail', '0009_newslettersubscriber_alter_subscriber_audience'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='sent_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
