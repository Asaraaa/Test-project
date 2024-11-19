from django import forms
from .models import Review

class ProductSearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=255, required=False)
    min_price = forms.DecimalField(label='Min Price', required=False)
    max_price = forms.DecimalField(label='Max Price', required=False)
    category = forms.ChoiceField(label='Category', choices=[
        ('', 'All'),
        ('book', 'Book'),
        ('clothes', 'Clothes'),
        ('art', 'Art'),
    ], required=False)

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']  
