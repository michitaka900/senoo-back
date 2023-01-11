from django.db import models


class Product(models.Model):
    STOCK_STATUS = [
        ('active', '出品中'),
        ('archived', '停止中'),
        ('draft', '準備中'),
    ]
    id = models.BigIntegerField(primary_key=True)
    handle = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STOCK_STATUS)
    price = models.CharField(max_length=20, null=True, blank=True)
    sku = models.CharField(max_length=255, null=True, blank=True)
    inventory_item_id = models.BigIntegerField()

    def __str__(self):
        return self.handle


class Image(models.Model):
    class Meta:
        ordering = ['position']

    id = models.BigIntegerField(primary_key=True)
    src = models.CharField(max_length=255)
    position = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    product = models.ForeignKey(
        Product, related_name='images', on_delete=models.CASCADE)