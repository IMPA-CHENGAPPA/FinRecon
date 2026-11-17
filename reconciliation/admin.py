from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Transaction, ReconciliationRecord

admin.site.register(Transaction)
admin.site.register(ReconciliationRecord)


