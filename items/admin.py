from django import forms
from django.contrib import admin

# Register your models here.
from django.db import models
from django.utils.html import format_html

from .forms import ImageForm, ImageWidget
from .models import Item, Image


class ImageInline(admin.TabularInline):
    model = Image
    fk_name = 'item'
    min_num = 1
    max_num = 4
    extra = 0
    formfield_overrides = {models.ImageField: {'widget': ImageWidget}}


class ItemAdmin(admin.ModelAdmin):
    model = Item

    list_display = ['name', 'price', 'image_tag', '__str__', 'category']

    class Meta:
        model = Item

    readonly_fields = []
    inlines = [ImageInline]
    list_filter = ['price']
    search_fields = ['name']

    def image_tag(self, obj):
        if obj and obj.images.exists():
            image = obj.images.first()
            return format_html(
                '<img src="{image_path}" alt="No image" width="100" height="50">'.format(
                    image_path=image.source.url))
        else:
            return None
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def has_change_permission(self, request, obj=None):
        return True


class ImageAdmin(admin.ModelAdmin):
    form = ImageForm


admin.site.register(Item, ItemAdmin)
