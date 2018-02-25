from django.shortcuts import render

# Create your views here.

# common urls

def home(request):
	''' home route '''
	return render(request, 'blog/home.html.j2', context={
		'title' : "Blog Home"
		})


def category(request, category_name):
	''' category route '''
	return render(request, 'blog/category.html.j2', context={
		'title' : "Blog Category - " + category_name
		})


def post(request, category_name, post_uid):
	''' post route '''
	return render(request, 'blog/post.html.j2', context={
		'title' : "Post - " + category_name + " :: " + str(post_uid)
		})

# admin urls

def edit_category(request):
	''' edit_category route '''
	return render(request, 'blog/admin/edit_category.html.j2', context={
		'title' : "Edit Category"
		})


def edit_posts(request):
	''' edit_posts route '''
	return render(request, 'blog/admin/edit_posts.html.j2', context={
		'title' : "Posts Overview"
		})


def edit_post(request, post_uid):
	''' edit_post route '''
	return render(request, 'blog/admin/edit_post.html.j2', context={
		'title' : "Edit Post - " + str(post_uid)
		})


def statistics(request):
	''' statistics route '''
	return render(request, 'blog/admin/statistics.html.j2', context={
		'title' : "Statistics"
		})

def ads(request):
	''' ads route '''
	return render(request, 'blog/admin/ads.html.j2', context={
		'title' : "Ads"
		})
