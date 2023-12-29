"""
View code
"""

import datetime
from flask import render_template, session

def render_po_template(template, **context):
    """ Pass a template (html) and a dictionary """
    if not context:
        context = {}
    now = datetime.datetime.now()
    context['year'] = now.year

    if 'userId' in session:
        context['loggedin'] = True

    return render_template(template, **context)
