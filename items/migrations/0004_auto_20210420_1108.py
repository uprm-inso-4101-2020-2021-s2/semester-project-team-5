# Generated by Django 3.2 on 2021-04-20 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0003_auto_20210420_0315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='item',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]