"""
urls
"""
from webapp2 import Route
from webapp2_extras.routes import RedirectRoute

ROUTES = [
    Route(r'/api/v1/purchase/create/', handler='app.views.api.v1.purchases.PurchaseCreateApi'),
    Route(r'/api/v1/purchase/create/interim/', handler='app.views.api.v1.purchases.CreateInterimPurchaseApi'),
    Route(r'/api/v1/purchase/accept/<po_id:.{12}>/', handler='app.views.api.v1.purchases.PurchaseAcceptApi'),
    Route(r'/api/v1/purchase/cancel/<po_id:.{12}>/', handler='app.views.api.v1.purchases.PurchaseCancelApi'),
    Route(r'/api/v1/purchase/deny/<po_id:.{12}>/', handler='app.views.api.v1.purchases.PurchaseDenyApi'),
    Route(r'/api/v1/purchases/get/', handler='app.views.api.v1.purchases.PurchaseGetApi'),
    Route(r'/api/v1/purchase/invoice/<po_id:.{12}>/', handler='app.views.api.v1.purchases.PurchaseInvoiceApi'),

    RedirectRoute(r'/purchase/', handler='app.views.purchase.PurchaseListView',
        strict_slash=True, name='list_purchases'),
    RedirectRoute(r'/purchase/create/', handler='app.views.purchase.PurchaseCreateView',
        strict_slash=True, name='create_purchase'),
    RedirectRoute(r'/purchase/<po_id:.{12}>/', handler='app.views.purchase.PurchaseView',
        strict_slash=True, name='view_purchase'),

    RedirectRoute('/user/new/', handler='app.views.user.NewUserView',
        strict_slash=True, name='new_user'),

    Route(r'/', handler='app.views.main.MainView', name='index'),
]
