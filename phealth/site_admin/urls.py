from django.urls import path, include
from django.conf.urls import include, url

from . import views

app_name = "site_admin"

dashboard_routes = [
	url(r'^$', views.dashboard, name='dashboard_home'),
	url(r'^cms/?$', views.cms, name='cms'),
	url(r'^tokens/?$', views.tokens, name='tokens'),
]

urlpatterns = [
    url(r'^cms_add/', views.cms_add, name='cms_add'),
    url(r'^signup/?$', views.SignUp, name='signup'),
    url(r'^signin/?$', views.SignIn, name='signin'),
    url(r'^dashboard/', include(dashboard_routes)),
]

