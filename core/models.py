from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100)
    # user optional: si no quieres manejar usuarios ahora, permite null
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return self.name

class Transaction(models.Model):
    TYPE_CHOICES = (('income','Income'),('expense','Expense'))
    # Para prototipo: si no quieres lidiar con usuarios, pon null=True y blank=True
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions', null=True, blank=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, related_name='transactions')
    description = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} - {self.type} - {self.amount}"
