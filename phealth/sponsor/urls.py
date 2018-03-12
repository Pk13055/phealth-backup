from django.urls import path, include
from django.conf.urls import include, url

from . import views

app_name = "sponsor"

dashboard_urls = [
    # home
	url(r'^$', views.dashboard, name='dashboard_home'),

    # account
    url(r'^account/basic/?$', views.basic, name='basic'),
    url(r'^account/pocs/?$', views.POCTableView.as_view(), name='contact'),
    url(r'^account/pocs/add?$', views.add_poc, name='add_poc'),    
    url(r'^account/organization/?$', views.organization, name='organization'),

    # payments
    url(r'^payments/?$', views.PaymentsTableView.as_view(), name='payments_view'),
    url(r'^payments/new/?$', views.payments_new, name='payments_new'),
    path('payments/add/<str:type>/<uuid:package_id>/', views.payments_add, name='payments_add'),

    # participants
    url(r'^participants/?$', views.ParticipantsTableView.as_view(), name='participants_view'),
    url(r'^participants/new/?$', views.user_view, name='participants_new'),
]

urlpatterns = [
    url(r'^signup/?$', views.SignUp, name='signup'),
    url(r'^signin/?$', views.SignIn, name='signin'),
    url(r'^dashboard/', include(dashboard_urls))
]
