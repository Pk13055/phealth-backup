from django.urls import path, include
from django.conf.urls import include, url

from . import views

app_name = "sponsor"

account_urls = [
    url(r'^basic/?$', views.account_basic, name='basic'),
    url(r'^pocs/?$', views.POCTableView.as_view(), name='contact'),
    url(r'^pocs/add/?$', views.add_poc, name='add_poc'),
    url(r'^organization/?$', views.account_organization, name='organization'),
]

payment_urls = [
    url(r'^$', views.PaymentsTableView.as_view(), name='payments_view'),
    url(r'^new/?$', views.payments_new, name='payments_new'),
    path('payments/add/<str:type>/<uuid:package_id>/', views.payments_add, name='payments_add'),
]

dashboard_urls = [
	url(r'^$', views.dashboard, name='dashboard_home'),
    url(r'account/', include(account_urls)),
    url(r'payments/', include(payment_urls)),
    url(r'^participants/?$', views.ParticipantsTableView.as_view(), name='participants_view'),
    url(r'^participants/new/?$', views.user_view, name='participants_new'),
]

urlpatterns = [
    url(r'^signup/?$', views.SignUp, name='signup'),
    url(r'^signin/?$', views.SignIn, name='signin'),
    url(r'^dashboard/', include(dashboard_urls))
]
