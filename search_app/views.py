from django.shortcuts import render
from .models import Product
from .forms import ProductSearchForm

def product_search(request):
    form = ProductSearchForm(request.GET or None)
    products = Product.objects.all()

    # 並び順の取得（デフォルトは名前順）
    sort = request.GET.get('sort', 'name')

    if sort == 'name':
        products = products.order_by('name')  # 名前順
    elif sort == 'price_asc':
        products = products.order_by('price')  # 価格の安い順
    elif sort == 'price_desc':
        products = products.order_by('-price')  # 価格の高い順
    elif sort == 'release_date_desc':
        products = products.order_by('-release_date')  # 発売日が新しい順
    elif sort == 'release_date_asc':
        products = products.order_by('release_date')  # 発売日が古い順

    if form.is_valid():
        query = form.cleaned_data.get('query')
        if query:
            products = products.filter(name__icontains=query)

        min_price = form.cleaned_data.get('min_price')
        if min_price:
            products = products.filter(price__gte=min_price)

        max_price = form.cleaned_data.get('max_price')
        if max_price:
            products = products.filter(price__lte=max_price)

        category = form.cleaned_data.get('category')
        if category:
            products = products.filter(category=category)

    return render(request, 'product_search.html', {'form': form, 'products': products})

