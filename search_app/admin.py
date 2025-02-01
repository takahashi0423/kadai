from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Category

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'release_date', 'image_display')  # 🔹 発売日を追加＆画像をサムネイルで表示
    list_filter = ('category', 'release_date')  # 🔹 カテゴリー・発売日でフィルタリング
    search_fields = ('name',)  # 🔹 商品名で検索可能
    fields = ('name', 'description', 'price', 'category', 'image', 'release_date')  # 🔹 管理画面の編集項目

    def image_display(self, obj):
        """Django管理画面で画像をサムネイル表示"""
        if obj.image:
            return format_html('<img src="{}" style="width:50px; height:auto;" />', obj.image.url)
        return "なし"

    image_display.short_description = '画像'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
