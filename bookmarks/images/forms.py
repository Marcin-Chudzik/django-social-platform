from urllib.request import Request, urlopen
from django import forms
from django.core.files.base import ContentFile
from django.utils.text import slugify

from .models import Image


class ImageCreateForm(forms.ModelForm):
    url = forms.CharField(label='', widget=forms.HiddenInput)

    class Meta:
        model = Image
        fields = ('title', 'url', 'description')

    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError(
                'The URL provided contains a file \
                 in the wrong format (.JPG or .JPEG).')
        return url

    def save(self, commit=True, force_insert=False, force_update=False):
        image = super(ImageCreateForm, self).save(commit=False)
        image_url = self.cleaned_data['url']
        image_name = f"{slugify(image.title)}." \
                     f"{image_url.rsplit('.', 1)[1].lower()}"

        # Downloading image from url
        req = Request(image_url, headers={"User-Agent": "Mozilla/5.0"})
        response = urlopen(req).read()
        image.image.save(image_name, ContentFile(response), save=False)
        if commit:
            image.save()
        return image
