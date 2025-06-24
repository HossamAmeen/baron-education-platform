from django.contrib import admin
from payments.models import Transaction
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "amount",
        "status",
        "created",
        "modified",
    )
    search_fields = ("user", "amount", "status")
    list_filter = ("status",)
    
