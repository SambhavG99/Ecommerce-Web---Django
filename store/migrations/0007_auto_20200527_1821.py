# Generated by Django 2.1.5 on 2020-05-27 12:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_shippingaddress_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentorder',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='paymentorder',
            name='currency',
        ),
        migrations.RemoveField(
            model_name='paymentorder',
            name='payment_capture',
        ),
        migrations.AddField(
            model_name='paymentorder',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.Customer'),
        ),
        migrations.AddField(
            model_name='paymentorder',
            name='payment_id',
            field=models.CharField(default=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='paymentorder',
            name='order',
            field=models.ForeignKey(default=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.Order'),
        ),
    ]
