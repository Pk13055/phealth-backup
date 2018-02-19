"""phealth URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import include, url
from common import views as common

urlpatterns = [

    url(r'^$', common.home_route, name='home'),
    url(r'^api/', include('api.urls', namespace='api')),
    url(r'^common/', include('common.urls', namespace='common')),

    url(r'^admin/', admin.site.urls),
    url(r'^site_admin/', include('site_admin.urls', namespace='site_admin')),

    url(r'^clinician/', include('clinician.urls', namespace='clinician')),
    url(r'^healthprovider/', include('healthprovider.urls', namespace='healthprovider')),

    url(r'^sponsor/', include('sponsor.urls', namespace='sponsor')),
    url(r'^reseller/', include('reseller.urls', namespace='reseller')),
    url(r'^salesagent/', include('salesagent.urls', namespace='salesagent')),
]
