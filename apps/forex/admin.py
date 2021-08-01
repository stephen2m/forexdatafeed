from django.contrib import admin

from apps.forex.models import ForexQuote


class ForexQuoteAdmin(admin.ModelAdmin):
    list_display = (
        'created_at',
        'currency_from',
        'currency_to',
        'exchange_rate',
        'bid_price',
        'ask_price',
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(ForexQuote, ForexQuoteAdmin)
