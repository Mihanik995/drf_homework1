# Generated by Django 5.0.6 on 2024-06-05 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_payment_summ'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='summ',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
