from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Cart, Review
from .forms import ProductSearchForm, ReviewForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = product.reviews.all()  # 商品のレビューを取得
    avg_rating = product.average_rating()  # 平均評価を取得

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = ReviewForm()

    return render(request, 'product_detail.html', {
        'product': product,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'form': form,
    })

def product_search(request):
    form = ProductSearchForm(request.GET or None)
    products = Product.objects.all()

    # 並び順の取得（デフォルトは名前順）
    sort = request.GET.get('sort', 'name')

    # **🔹 並び順を適用**
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

    # **🔹 検索条件の適用**
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

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # すでにカートに入っている場合は数量を増やす
    cart_item, created = Cart.objects.get_or_create(product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    return JsonResponse({"message": "カートに追加しました", "cart_count": Cart.objects.count()})

def cart_view(request):
    cart_items = Cart.objects.all()
    return render(request, 'cart.html', {'cart_items': cart_items})

def remove_from_cart(request, product_id):
    """🛒 カートから商品を削除"""
    cart_item = get_object_or_404(Cart, product_id=product_id)
    
    if cart_item.quantity > 1:
        cart_item.quantity -= 1  # 商品の数量を減らす
        cart_item.save()
    else:
        cart_item.delete()  # 数量が1なら削除
    
    return JsonResponse({"message": "カートから削除しました", "cart_count": Cart.objects.count()})
