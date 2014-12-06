"""
Jinja2 filters
"""

def format_currency(value):
    return "${:,.2f}".format(value)
    
def pad_zeros(value):
    return str(value).zfill(4)
