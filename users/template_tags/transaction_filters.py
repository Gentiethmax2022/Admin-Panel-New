from django import template

register = template.Library()

@register.filter
def filter_status(transactions, status):
    return [transaction for transaction in transactions if transaction.status == status]


