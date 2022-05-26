from django import template
from api.models import *

register = template.Library()

@register.simple_tag(name='get_bankcards')
def get_cards():
    return BankCard.objects.all()


@register.inclusion_tag('api/base.html')
def show_cards(sort=None, card_selected=0):
    if not filter:
        cards = BankCard.objects.all()
    else:
        cards = BankCard.objects.filter(sort)
    return {'cards':cards, 'card_selected':card_selected}