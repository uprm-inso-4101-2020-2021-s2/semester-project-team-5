# Generated by Django 3.1.6 on 2021-02-27 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0002_item_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='items/'),
        ),
    ]