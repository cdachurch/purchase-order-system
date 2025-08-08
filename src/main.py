from flask import Flask, url_for
from authlib.integrations.flask_client import OAuth

# Imports the Cloud Logging client library
import google.cloud.logging

from app.views import auth, purchase, render_po_template, user
from app.views.api.v1 import purchases as purchases_api
from app.views.filters import format_currency, pad_zeros, copyright_year
from app.workflow.user import get_log_in_out_links_and_user

import settings

# Instantiates a client
client = google.cloud.logging.Client()

# Retrieves a Cloud Logging handler based on the environment
# you're running in and integrates the handler with the
# Python logging module. By default this captures all logs
# at INFO level and higher
client.setup_logging()

app = Flask(__name__)
app.jinja_env.filters.update(
    {
        "currency": format_currency,
        "pad": pad_zeros,
        "copyright": copyright_year,
    }
)
app.secret_key = settings.SESSION_SECRET


@app.route("/")
def index():
    return render_po_template("index.html", **(get_log_in_out_links_and_user()))


app.register_blueprint(auth.bp)
app.register_blueprint(purchase.bp)
app.register_blueprint(user.bp)
app.register_blueprint(purchases_api.bp)

oauth = OAuth(app)
oauth.register(
    name="basecamp",
    client_id=settings.BASECAMP_CLIENT_ID,
    client_secret=settings.BASECAMP_CLIENT_SECRET,
    authorize_url="https://launchpad.37signals.com/authorization/new?type=web_server",
    access_token_url="https://launchpad.37signals.com/authorization/token?type=web_server",
)


@app.route("/bclogin")
def basecamp_login():
    redirect_uri = url_for("basecamp_callback", _external=True)
    return oauth.basecamp.authorize_redirect(redirect_uri=redirect_uri)


@app.route("/bccallback", methods=["GET", "POST"])
def basecamp_callback():
    try:
        token = oauth.basecamp.authorize_access_token(
            client_id=settings.BASECAMP_CLIENT_ID,
            client_secret=settings.BASECAMP_CLIENT_SECRET,
        )

        return token, 200
    except Exception as e:
        print(f"Exception in basecamp_callback: {e}")
        import traceback

        traceback.print_exc()
        return f"Error: {str(e)}", 500
