from django.contrib import admin

from payments.models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "amount",
        "currency",
        "gateway_transaction_id",
        "client_secret",
        "reference_id",
        "status",
        "created",
        "modified",
    )
    search_fields = ("user", "amount", "status")
    list_filter = ("status",)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
