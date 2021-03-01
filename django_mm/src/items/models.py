import random
import os
from django.db import models
from ecommerce import settings


# Writing in the fields that are going to be on the database


# 2 functions to change the name of the file
# This is made for no error in image loading
def get_ext_from_file(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 203033993933)
    name, ext = get_ext_from_file(filename)
    f_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "item/{new_filename}/{f_filename}".format(new_filename=new_filename, f_filename=f_filename)


class Item(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='items', null=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    quantity = models.IntegerField(default=1, null=False)
    Category = models.CharField(max_length=20, null=False, default='')

    def __str__(self):
        return self.name


class Image(models.Model):
    item = models.ForeignKey(Item, models.CASCADE, related_name='images', null=False)
    # image pillow needed to be install and it becomes a requirement
    source = models.ImageField(upload_to=upload_image_path, null=False, blank=False)


