# Generated by Django 3.1.6 on 2021-02-27 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0004_auto_20210227_0225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.FileField(null=True, upload_to='item/'),
        ),
    ]