import json
from django import forms
from django.shortcuts import render
from django.http import Http404
from django_summernote.widgets import SummernoteWidget
from django_tables2 import RequestConfig
from .tables import PostTable
from api.models import Post, BlogCategory, BlogComment, CDN

# Create your views here.

# common urls

def get_categories():  #gets the categories which need to rendered on all the user side routes
	return [_['name'] for _ in BlogCategory.objects.values('name')]

def home(request):
	''' home route ''' 
	# c = BlogComment.objec 
	categories = []
	for cat in BlogCategory.objects.all():
		cur_cat = {
			'name' : cat.name,
			'color' : cat.color,
			'featured_posts' : []
		}
		for post in cat.featured_posts.all():
			cur_post = {
			'uid' : post.uid,
			'title' : post.title,
			'image' : post.image,
			'content' : post.content,
			'date_added' : post.date_added,
			}
			cur_cat['featured_posts'].append(cur_post)
		categories.append(cur_cat)
	print(categories)
	return render(request, 'blog/home.html.j2', context={
		'title' : "Blog Home",
		'categories' : get_categories(),
		'category_posts' : categories,
		})


def category(request, category_name):
	category = BlogCategory.objects.filter(name = category_name).first()
	print(category)
	f = category.featured_posts.all()
	print(f)
	if request.method == "POST":
		print(POST)

	return render(request, 'blog/category.html.j2', context={
		'title' : "Blog Category - " + category_name,
		'categories' : get_categories(),
		'posts' : f,
		'category_name': category_name.title(),
		})


def post(request, category_name, post_uid):
	''' post route '''
	# u = User.objects.filter(email=request.session['email']).first()
	comments = []
	p = Post.objects.filter(uid=post_uid).first()
	c = BlogComment.objects.filter(post__uid=post_uid).all()
	for cat in c:
		cur_cat = {
			'text' : cat.text,
			'name' : cat.user.name,
		}
	class BlogCommentForm(forms.ModelForm):
		class Meta:
			model = BlogComment
			fields = ('text',)
			widgets = {
				'text' : SummernoteWidget(),
			}

	post = BlogCommentForm()

	if request.method == 'POST':
		b = BlogCommentForm(request.POST)
		if b.is_valid():
			comment = b.save(commit=False)
			comment.post = p
			# comment.user = u\
			comment.save()
		post = b


	return render(request, 'blog/post.html.j2', context={
		'title' : "Post - " + category_name + " :: " + str(post_uid),
		'categories' : get_categories(),
		'post' : post,
		'comments' : c,
		})

# admin urls

def edit_category(request):
	''' edit_category route '''

	class CategoryForm(forms.ModelForm):

		featured_posts = forms.ModelMultipleChoiceField(
			widget=forms.CheckboxSelectMultiple,
			required=False, queryset=None)

		def __init__(self, *args, **kwargs):
			super(CategoryForm, self).__init__(*args, **kwargs)
			self.fields['featured_posts'].queryset = Post.objects.filter(category=self.instance)

		class Meta:
			model = BlogCategory
			fields = ('id', 'name', 'color', 'featured_posts',)

	EditForm = forms.modelformset_factory(model=BlogCategory, form=CategoryForm, extra=0)
	form_set = EditForm()

	if request.method == "POST":
		edit_formset = EditForm(request.POST, request.FILES)
		if edit_formset.is_valid():
			edit_formset.save()
		else:
			print(edit_formset.errors)

		form_set = edit_formset

	return render(request, 'blog/admin/edit_category.html.j2', context={
		'title' : "Edit Categories",
		'edit_set' : form_set,
		'colors' : ['success', 'info', 'warning', 'danger']
		})


def edit_posts(request):
	# posts = PostTable(Post.objects.all())
	# RequestConfig(request, paginate={'per_page': 5}).configure(posts)

	posts = PostTable()

	return render(request, 'blog/admin/edit_posts.html.j2', context={
		'title' : "Posts Overview",
		'posts' : posts,
		})


def edit_post(request, post_uid):
	''' edit_post route '''
	try:
		p = Post.objects.get(uid=post_uid)
	except:
		raise Http404

	class EditPostForm(forms.ModelForm):

		class Meta:
			model = Post
			fields = ('__all__')
			widgets = {
				'content' : SummernoteWidget()
			}

	edit_form = EditPostForm(instance=p)

	if request.method == "POST":
		form = EditPostForm(request.POST, request.FILES, instance=p)
		if form.is_valid():
			form.save()
		edit_form = form

	return render(request, 'blog/admin/edit_post.html.j2', context={
		'title' : "Blog - Edit Post",
		'post' : edit_form
		})


def statistics(request):
	''' statistics route '''
	cats = BlogCategory.objects.all()
	posts = Post.objects.values_list('uid', 'title', 'clicks',
		'category', 'date_added', 'date_modified')
	categories = []
	for cat in cats:
		cur_posts = posts.filter(category=cat.id)
		current_cat = {
			'title' : cat.name,
			'color' : cat.color,
			'clicks' : sum([_['clicks'] for _ in
				cur_posts.values('clicks')]),
			'posts' : []
		}
		for post in cur_posts:
			uid, title, clicks, category, date_added, date_modified = post
			current_cat['posts'].append({
				'uid' : str(uid),
				'title' :  title,
				'clicks' :  clicks,
				'category' :  cat.name,
				'date_added' : date_added,
				'date_modified' : date_modified,
				})
		categories.append(current_cat)

	return render(request, 'blog/admin/statistics.html.j2', context={
		'title' : "Statistics",
		'sections' : categories,
		'colors' : ['success', 'info', 'warning', 'danger']
		})

def ads(request):
	''' ads route '''
	class AdForm(forms.ModelForm):

		class Meta:

			model = CDN
			fields = ('image',)

	form_ad = AdForm()

	if request.method == 'POST':
		print('inside POST function')
		print(request.POST)

		a = AdForm(request.POST, request.FILES)

		if a.is_valid():
			ad = a.save(commit=False)
			ad.code = request.POST['code'][0]
			ad.save()
		else:
			print('Form entries not valid')

	return render(request, 'blog/admin/ads.html.j2', context={
		'title' : "Ads",
		'form_ad': form_ad,
		})
