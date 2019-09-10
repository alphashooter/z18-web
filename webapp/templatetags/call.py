from django.template import Library

register = Library()


@register.filter(name='convert_price')
def convert_price(product, user):
    return product.convert_price(user)
