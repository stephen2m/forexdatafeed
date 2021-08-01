import uuid

from django.db import models


class ForexQuote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    currency_from = models.CharField('currency converting from', max_length=5)
    currency_to = models.CharField('currency converting to', max_length=5)
    exchange_rate = models.DecimalField(max_digits=19, decimal_places=2)
    bid_price = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    ask_price = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField('created at', editable=False, db_index=True, auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.currency_from} to {self.currency_to} @ {self.exchange_rate}'
