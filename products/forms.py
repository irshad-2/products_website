from django import forms

from products.models import Product


class ProductForm(forms.ModelForm):
    tags = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input'}), label="Category")

    class Meta:
        model = Product
        exclude = ("brand", "is_deleted", "categories")

        widgets = {
            "title": forms.TextInput(attrs={'class': 'input'}),
            "short_descriptions": forms.Textarea(attrs={'class': 'input'}),
        }
