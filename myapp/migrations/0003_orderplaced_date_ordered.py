# Generated by Django 4.1.7 on 2023-05-02 09:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_orderplaced'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderplaced',
            name='date_ordered',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
