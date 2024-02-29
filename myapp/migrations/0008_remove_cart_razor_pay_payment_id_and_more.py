# Generated by Django 4.1.7 on 2024-02-27 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_cart_payment_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='razor_pay_payment_id',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='razor_pay_payment_signature',
        ),
        migrations.AddField(
            model_name='orderplaced',
            name='payment_status',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='orderplaced',
            name='razor_pay_order_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='orderplaced',
            name='razor_pay_payment_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='orderplaced',
            name='razor_pay_payment_signature',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]