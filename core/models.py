# core/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return self.name

class Transaction(models.Model):
    TYPE_CHOICES = (('income','Income'),('expense','Expense'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions', null=True, blank=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, related_name='transactions')
    description = models.CharField(max_length=500, blank=True)
    # <-- Cambio aquí: usar default en lugar de auto_now_add
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} - {self.type} - {self.amount}"

class ExportReport(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='export_reports')
    name = models.CharField(max_length=200)
    format = models.CharField(max_length=10, choices=[('csv', 'CSV'), ('json', 'JSON'), ('pdf', 'PDF')])
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    transactions_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    file_path = models.CharField(max_length=500, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} - {self.name} ({self.format})"
    
    @property
    def period(self):
        if self.start_date and self.end_date:
            return f"{self.start_date} a {self.end_date}"
        elif self.start_date:
            return f"Desde {self.start_date}"
        elif self.end_date:
            return f"Hasta {self.end_date}"
        return "Todas las transacciones"
