# Generated by Django 4.1.7 on 2024-02-27 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_cart_razor_pay_order_id_cart_razor_pay_payment_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='payment_status',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
