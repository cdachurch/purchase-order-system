""" superadmin.py """
from app.views import TemplatedView


class IndexView(TemplatedView):
    """
    Superadmin home page
    """
    def get(self):
        """ GET """
        return self.render_response('superadmin/index.html')
