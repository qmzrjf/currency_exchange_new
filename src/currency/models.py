from django.db import models

from currency import model_choices as mch
from django.utils import timezone

from django.core.cache import cache

from currency.utils import generate_rate_cache_key


class Rate(models.Model):
    created = models.DateTimeField(default=timezone.now)
    currency = models.PositiveSmallIntegerField(choices=mch.CURRENCY_CHOICES)
    source = models.PositiveSmallIntegerField(choices=mch.SOURCE_CHOICES)
    buy = models.DecimalField(max_digits=4, decimal_places=2)
    sale = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f'{self.get_currency_display()} {self.get_source_display()} {self.buy} {self.sale} {self.created} '

    def save(self, *args, **kwargs):
        if not self.id:
            cache_key = generate_rate_cache_key(self.source, self.currency)
            cache.delete(cache_key)
        super().save(*args, **kwargs)
