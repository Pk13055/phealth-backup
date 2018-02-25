from django.urls import path, include
from django.conf.urls import include, url

from . import views

app_name = "blog"

admin_urls = [
	url(r'^$', views.statistics, name='dashboard_home'),
	url(r'categories/?$', views.edit_category, name='edit_category'),
	url(r'posts/?$', views.edit_posts, name='edit_posts'),
	path('posts/<uuid:post_uid>/', views.edit_post, name='edit_post'),
	url(r'statistics/?$', views.statistics, name='statistics'),
	url(r'ads/?$', views.ads, name='ads'),
]

urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^admin/', include(admin_urls)),
	path('<str:category_name>/', views.category, name='category'),
	path('<str:category_name>/<uuid:post_uid>/', views.post, name='home'),
]

