import random
import os
from django.db import models
from django.urls import reverse
from ecommerce import settings
from django.db.models import Q

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


class ItemManager(models.Manager):

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None


    def search(self, query):
        lookups = Q(category__icontains=query) | Q(name__icontains=query) | Q(description__icontains=query)
        return self.get_queryset().filter(lookups).distinct()


CATEGORY_TECHNOLOGY = '0'
CATEGORY_HOME_AND_GARDEN = '1'
CATEGORY_PARTS_ACCESSORIES = '2'
CATEGORY_TOYS = '3'
CATEGORY_MUSIC = '4'
CATEGORY_JEWELRY = '5'
CATEGORY_CLOTHES = '6'
CATEGORY_OTHERS = '7'
CATEGORY_BEAUTY = '8'

CATEGORY = {
    CATEGORY_TECHNOLOGY: 'Technology',
    CATEGORY_HOME_AND_GARDEN: 'Home & Garden',
    CATEGORY_PARTS_ACCESSORIES: 'Parts & Accessories',
    CATEGORY_TOYS: 'Toys',
    CATEGORY_MUSIC: 'Music',
    CATEGORY_JEWELRY: 'Jewelry',
    CATEGORY_CLOTHES: 'Clothes',
    CATEGORY_BEAUTY: 'Makeups & Beauty',
    CATEGORY_OTHERS: 'Others'
}


class Item(models.Model):
    CATEGORY_CHOICES = (
        (CATEGORY_TECHNOLOGY, CATEGORY[CATEGORY_TECHNOLOGY]),
        (CATEGORY_HOME_AND_GARDEN, CATEGORY[CATEGORY_HOME_AND_GARDEN]),
        (CATEGORY_PARTS_ACCESSORIES, CATEGORY[CATEGORY_PARTS_ACCESSORIES]),
        (CATEGORY_TOYS, CATEGORY[CATEGORY_TOYS]),
        (CATEGORY_MUSIC, CATEGORY[CATEGORY_MUSIC]),
        (CATEGORY_JEWELRY, CATEGORY[CATEGORY_JEWELRY]),
        (CATEGORY_CLOTHES, CATEGORY[CATEGORY_CLOTHES]),
        (CATEGORY_BEAUTY, CATEGORY[CATEGORY_BEAUTY]),
        (CATEGORY_OTHERS, CATEGORY[CATEGORY_OTHERS]),
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='items', null=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    quantity = models.IntegerField(default=1, null=False)
    category = models.CharField(max_length=20, null=False, default=0, choices=CATEGORY_CHOICES)
    objects = ItemManager()

    def get_absolute_url(self):
        return "{url}?category={category}".format(url=reverse("items:details", args=(self.pk,)),
                                                   category=self.get_category_text())

    def get_category_text(self):
        return CATEGORY[self.category]

    def __str__(self):
        return self.name


class Image(models.Model):
    item = models.ForeignKey(Item, models.CASCADE, related_name='images', null=False)
    # image pillow needed to be installed and it becomes a requirement
    source = models.ImageField(upload_to=upload_image_path, null=False, blank=False)

    def delete(self, using=None, keep_parents=False):
        image_path = settings.MEDIA_ROOT + self.source.url
        os.remove(image_path)
        return super().delete(using, keep_parents)


