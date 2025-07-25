# Generated by Django 5.2.1 on 2025-07-07 17:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sendemail', '0008_alter_subscriber_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsletterSubscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, null=True)),
                ('name', models.CharField(blank=True, max_length=255)),
                ('subscribed', models.BooleanField(default=True)),
                ('subscribed_at', models.DateTimeField(auto_now_add=True)),
                ('unsubscribed_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='audience',
            field=models.ForeignKey(default=85, on_delete=django.db.models.deletion.CASCADE, related_name='subscribers', to='sendemail.audience'),
        ),
    ]
