# Generated by Django 2.1.5 on 2020-05-27 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_paymentorder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentorder',
            name='currency',
            field=models.CharField(default='INR', max_length=200, null=True),
        ),
    ]
