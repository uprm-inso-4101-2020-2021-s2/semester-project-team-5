# Generated by Django 3.1.6 on 2021-02-27 02:56

from django.db import migrations, models
import items.models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0006_auto_20210227_0245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(null=True, upload_to=items.models.upload_image_path),
        ),
    ]
