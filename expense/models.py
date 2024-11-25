from django.db import models
import uuid

class Expense(models.Model):
    expense_name = models.CharField(max_length=200)
    expense_category = models.CharField(max_length=200)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.expense_name+" "
