# Generated by Django 2.1.5 on 2020-05-27 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_auto_20200527_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='phone',
            field=models.IntegerField(blank=True, default='1234567890', null=True),
        ),
    ]
