from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.


def price_validator(price: float):
    if price < 0:
        raise ValidationError('Price must be positive')


class Named(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Product(Named):
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[price_validator])

    def convert_price(self, user: User):
        currency = Currency.objects.get(pk=1)
        if not user.is_authenticated:
            return currency.format(self.price)
        try:
            profile = user.profile
        except User.profile.RelatedObjectDoesNotExist:
            return currency.format(self.price)
        currency = profile.currency
        return currency.format(self.price / profile.currency.exchange)


class Currency(Named):
    class Meta:
        verbose_name_plural = 'currencies'
    code = models.CharField(max_length=3)
    symbol = models.CharField(max_length=1, null=True)
    exchange = models.DecimalField(max_digits=8, decimal_places=4)

    def format(self, price):
        if self.symbol:
            return f'{self.symbol}{round(price, 2)}'
        else:
            return f'{round(price, 2)} {self.code}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.SET_DEFAULT, default=1)
