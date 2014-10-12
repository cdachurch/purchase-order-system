"""
User views
"""
from app.views import TemplatedView
from app.domain.user import get_current_user
from app.workflow.user import get_or_create_user, get_log_in_out_links_and_user

class NewUserView(TemplatedView):
    """ New user view, gets called when someone signs in """

    def get(self):
        """ GET """
        context = {}

        # Add the login/out links and the user info
        context.update(get_log_in_out_links_and_user())

        if context['in_datastore']:
            # Not making someone new, redirect back home
            self.redirect('/')
        else:
            context['new_user'] = True

        self.render_response("user.html", **context)

    def post(self):
        """ POST """
        name = self.request.POST.get('name')
        email = self.request.POST.get('email')
        users_user = get_current_user()

        # Acknowledging that it will return something, but have no use for it
        _ = get_or_create_user(name, email, users_user.user_id())

        new_context = {
            'name': name
        }

        self.redirect_to('index', **new_context)
