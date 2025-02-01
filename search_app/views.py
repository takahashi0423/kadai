from django.shortcuts import render
from .models import Product, Category
from .forms import ProductSearchForm

def product_search(request):
    form = ProductSearchForm(request.GET or None)
    products = Product.objects.all().order_by('name')  # 名前順に並べる（昇順）

    if form.is_valid():
        query = form.cleaned_data.get('query')  # キーワードを取得
        if query:
            products = products.filter(name__icontains=query)

        # min_priceを安全に取得
        min_price = form.cleaned_data.get('min_price')
        if min_price:
            products = products.filter(price__gte=min_price)

        # max_priceを安全に取得
        max_price = form.cleaned_data.get('max_price')
        if max_price:
            products = products.filter(price__lte=max_price)

        # カテゴリを安全に取得
        category = form.cleaned_data.get('category')
        if category:
            products = products.filter(category=category)

    return render(request, 'product_search.html', {'form': form, 'products': products})


def product_list(request):
    # すべての商品を名前順で取得
    products = Product.objects.all().order_by('name')  # 名前順に並べる（昇順）
    return render(request, 'product_list.html', {'products': products})
