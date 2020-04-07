from django.db import models

from currency import model_choices as mch
from datetime import date


class Rate(models.Model):
    created = models.DateTimeField(default=date.today)
    currency = models.PositiveSmallIntegerField(choices=mch.CURRENCY_CHOICES)
    source = models.PositiveSmallIntegerField(choices=mch.SOURCE_CHOICES)
    buy = models.DecimalField(max_digits=4, decimal_places=2)
    sale = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f'{self.get_currency_display()} {self.get_source_display()} {self.buy} {self.sale} {self.created} '
