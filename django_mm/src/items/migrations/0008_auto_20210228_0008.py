# Generated by Django 3.1.6 on 2021-02-28 00:08

from django.db import migrations, models
import items.models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0007_auto_20210227_0256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=items.models.upload_image_path),
        ),
    ]
