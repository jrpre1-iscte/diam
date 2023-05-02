from django import forms
from .models import CartItem


class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 10, 'value': 1}),
        }

class Purchase(models.Model):
    item = models.ForeignKey(ClothingItem, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.item.name} - {self.buyer.username}'

    class Meta:
        ordering = ['-date']


class PurchaseHistory(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.purchase.item.name} - {self.purchase.buyer.username} ({self.quantity})'


class PurchaseHistoryForm(forms.ModelForm):
    class Meta:
        model = PurchaseHistory
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 10, 'value': 1}),
        }
