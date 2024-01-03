from flask import Flask

from app.views import auth, purchase, render_po_template, user
from app.views.api.v1 import purchases as purchases_api
from app.views.filters import format_currency, pad_zeros, copyright_year
from app.workflow.user import get_log_in_out_links_and_user

import settings

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

# ROUTES = [
#     Route(r'/api/v1/purchase/create/', handler='app.views.api.v1.purchases.PurchaseCreateApi'),
#     Route(r'/api/v1/purchase/create/interim/', handler='app.views.api.v1.purchases.CreateInterimPurchaseApi'),
#     Route(r'/api/v1/purchase/accept/<po_id:.{12}>/', handler='app.views.api.v1.purchases.PurchaseAcceptApi'),
#     Route(r'/api/v1/purchase/cancel/<po_id:.{12}>/', handler='app.views.api.v1.purchases.PurchaseCancelApi'),
#     Route(r'/api/v1/purchase/deny/<po_id:.{12}>/', handler='app.views.api.v1.purchases.PurchaseDenyApi'),
#     Route(r'/api/v1/purchases/get/', handler='app.views.api.v1.purchases.PurchaseGetApi'),
#     Route(r'/api/v1/purchase/invoice/<po_id:.{12}>/', handler='app.views.api.v1.purchases.PurchaseInvoiceApi'),

#     RedirectRoute(r'/superadmin/', handler='app.views.superadmin.IndexView', strict_slash=True,
#                   name='superadmin_home'),

#     RedirectRoute(r'/purchase/', handler='app.views.purchase.PurchaseListView',
#                   strict_slash=True, name='list_purchases'),
#     RedirectRoute(r'/purchase/all/', handler='app.views.purchase.AllPurchaseListView',
#                   strict_slash=True, name='list_purchases'),
#     RedirectRoute(r'/purchase/create/', handler='app.views.purchase.PurchaseCreateView',
#                   strict_slash=True, name='create_purchase'),
#     RedirectRoute(r'/purchase/<po_id:.{12}>/', handler='app.views.purchase.PurchaseView',
#                   strict_slash=True, name='view_purchase'),

#     RedirectRoute('/user/new/', handler='app.views.user.NewUserView',
#                   strict_slash=True, name='new_user'),

#     Route(r'/', handler='app.views.main.MainView', name='index'),
# ]
