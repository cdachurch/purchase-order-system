"""
Main views
"""
import logging
import urllib

from app.views import TemplatedView
from app.workflow.user import get_log_in_out_links_and_user


class MainView(TemplatedView):
    """
    Main view routes
    """
    def get(self):
        """
        GET IT
        """
        context = {
            'bread_crumbs': [('Home', None)],
            'name': self.request.GET.get('name')
        }

        context.update(get_log_in_out_links_and_user())

        self.render_response("index.html", **context)
