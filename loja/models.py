from django.db import models
from django.contrib.auth.models import User


class ClothingItem(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    size = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='images/')
    sold = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class CartItem(models.Model):
    item = models.ForeignKey(ClothingItem, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.item.name}"


class Purchase(models.Model):
    item = models.ForeignKey(ClothingItem, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item.name} - {self.buyer.username}"
