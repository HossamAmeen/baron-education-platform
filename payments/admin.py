from django.contrib import admin

from payments.models import Transaction


from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user_email",
        "amount_with_currency",
        "gateway_transaction_id",
        "reference_id",
        "status_display",
        "created_formatted",
        "modified_formatted",
        "client_secret_short",
    )
    list_display_links = ("id", "user_email")
    search_fields = ("user__email", "amount", "status", "reference_id")
    list_filter = ("status", "currency", "created")
    list_per_page = 20
    readonly_fields = ("created", "modified", "client_secret")
    ordering = ("-created",)

    def user_email(self, obj):
        return obj.user.email if obj.user else "-"
    user_email.short_description = "User Email"
    user_email.admin_order_field = "user__email"

    def amount_with_currency(self, obj):
        return f"{obj.amount} {obj.currency}"
    amount_with_currency.short_description = "Amount"
    amount_with_currency.admin_order_field = "amount"

    def status_display(self, obj):
        color_map = {
            Transaction.TransactionStatus.FAILED: "red",
            Transaction.TransactionStatus.PENDING: "grey",
            Transaction.TransactionStatus.PAID: "green",
        }
        color = color_map.get(obj.status, "black")
        return format_html(
            '<span style="color:{}">{}</span>',
            color,
            obj.get_status_display()
        )
    status_display.short_description = "Status"
    status_display.admin_order_field = "status"

    def created_formatted(self, obj):
        return obj.created.strftime("%b %d, %Y, %I:%M %p")
    created_formatted.short_description = "Created"
    created_formatted.admin_order_field = "created"

    def modified_formatted(self, obj):
        return obj.modified.strftime("%b %d, %Y, %I:%M %p") if obj.modified else "-"
    modified_formatted.short_description = "Modified"
    modified_formatted.admin_order_field = "modified"

    def client_secret_short(self, obj):
        if obj.client_secret:
            return f"{obj.client_secret[:15]}..." if len(obj.client_secret) > 15 else obj.client_secret
        return "-"
    client_secret_short.short_description = "Client Secret"

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        if obj and obj.status == Transaction.TransactionStatus.PAID:
            return False
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("user")