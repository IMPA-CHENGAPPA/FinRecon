from django.db import models


class Transaction(models.Model):

    transaction_id = models.CharField(max_length=100)
    transaction_date = models.DateField()
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    source = models.CharField(max_length=50)
    status = models.CharField(max_length=30, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_id


class ReconciliationRecord(models.Model):

    transaction_id = models.CharField(max_length=100)

    bank_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    internal_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    status = models.CharField(max_length=30)

    exception_status = models.CharField(
        max_length=30,
        default="Open"
    )

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_id