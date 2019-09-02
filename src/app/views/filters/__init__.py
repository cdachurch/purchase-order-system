"""
Jinja2 filters
"""
import datetime


def format_currency(value):
    if not value:
        return 'None'
    return "${:,.2f}".format(value)


def pad_zeros(value):
    if not value:
        return ''
    return str(value).zfill(4)


def copyright_year(_):
    n = datetime.datetime.now()
    return n.year
