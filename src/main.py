import os

import set_sys_path # Must be done first to set up path

from webapp2 import WSGIApplication
from urls import ROUTES

from app.views.filters import format_currency, pad_zeros


TEMPLATE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            'templates')

CONFIG = {
    'webapp2_extras.jinja2': {
        'filters': {
            'currency': format_currency,
            'pad': pad_zeros,
        },
        'template_path': TEMPLATE_DIR
    }
}


APP = WSGIApplication(ROUTES, config=CONFIG)
