from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Safely get an item from a dictionary."""
    return dictionary.get(key)


@register.filter
def get_order(sort_option, order):
    return 'asc' if sort_option != 'number' or order == 'desc' else 'desc'

@register.filter
def set_value(value, new_value):
    return new_value

# @register.filter
# def distinct_years(queryset):
#     try:
#         return queryset.dates('date', 'year')
#     except FieldDoesNotExist:
#         return []  # Return an empty list if the field does not exist

# @register.filter
# def is_in_list(value, arg):
#     """Check if a value is in a comma-separated list."""
#     return value in arg.split(',')