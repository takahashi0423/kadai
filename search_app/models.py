from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    parent_category = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='subcategories'
    )

    def __str__(self):
        return self.name

from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    release_date = models.DateField(null=True, blank=True)  # 🔹 発売日を手動設定可能に

    def __str__(self):
        return self.name


image = models.ImageField(
    upload_to='product_images/',
    blank=True,
    null=True,
    default='product_images/default_image.png'  # デフォルト画像のパス
)
