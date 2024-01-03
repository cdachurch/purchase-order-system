"""
View code
"""

import datetime
from flask import render_template, session

from app.workflow.user import get_log_in_out_links_and_user


def render_po_template(template, **context):
    """Pass a template (html) and a dictionary"""
    if not context:
        context = {}
    now = datetime.datetime.now()
    context["year"] = now.year

    if "userId" in session:
        context["loggedin"] = True

    context.update(get_log_in_out_links_and_user())

    return render_template(template, **context)
