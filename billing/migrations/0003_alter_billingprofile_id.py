# Generated by Django 3.2 on 2021-04-20 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0002_billingprofile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billingprofile',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
