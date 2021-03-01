from django import forms
from django.forms import inlineformset_factory
from django.utils.safestring import mark_safe

from .models import Item, Image


def thumbnail(image_path, width, height):
    return '<img src="{image_path}" alt="{name}" class="widget-img" width="{width}" height="{height}"/>'.format(
        image_path=image_path, name=image_path, width=width, height=height)


class ImageWidget(forms.FileInput):
    template = '<div>{image}</div>' \
               '<div>{input}</div>'

    def __init__(self, attrs=None, template=template, width=200, height=150):
        if template is not None:
            self.template = template
        self.width = width
        self.height = height
        super(ImageWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None, renderer=None):
        input_html = super().render(name, value, attrs)
        if value and hasattr(value, 'width') and hasattr(value, 'height'):
            image_html = thumbnail(value.url, self.width, self.height)
            output = self.template.format(input=input_html,
                                          image=image_html)
        else:
            output = input_html
        return mark_safe(output)


class ImageForm(forms.ModelForm):
    image = forms.ImageField(widget=ImageWidget)

    class Meta:
        model = Image
        fields = '__all__'
        widgets = {
            'image': ImageWidget
        }


ImageFormSet = inlineformset_factory(Item, Image, form=ImageForm)