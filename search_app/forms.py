from django import forms
from .models import Category

class ProductSearchForm(forms.Form):
    query = forms.CharField(
        max_length=255,
        required=False,
        label='キーワード',
        widget=forms.TextInput(attrs={'placeholder': '商品名を入力'})
    )
    min_price = forms.DecimalField(
        required=False,
        max_digits=10,
        decimal_places=2,
        label='最低価格',
        widget=forms.NumberInput(attrs={'placeholder': '最低価格を入力'})
    )
    max_price = forms.DecimalField(
        required=False,
        max_digits=10,
        decimal_places=2,
        label='最高価格',
        widget=forms.NumberInput(attrs={'placeholder': '最高価格を入力'})
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label='カテゴリー',
        empty_label='すべて'
    )
    release_date = forms.DateField(
        required=False,
        label='発売日',
        widget=forms.DateInput(attrs={'type': 'date'})  # 🔹 カレンダー選択
    )
