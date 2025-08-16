from django.db import models

class Ledger(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    ledger = models.ForeignKey(Ledger, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField()
    transaction_type = models.CharField(max_length=20, choices=[
        ('income', 'Income'),
        ('expense', 'Expense')
    ], default='expense')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ledger.name} - {self.amount}"

class Report(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
