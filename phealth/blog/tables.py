from table import Table
from table.columns import *
from table.utils import A

from api.models import BlogComment, BlogCategory, Post

class PostTable(Table):
	'''
	table for blog posts
	'''

	title = Column(field='title', header='Title')
	category = Column(field='category', header='Category')
	clicks = Column(field='clicks', header='Clicks')
	date_added = DatetimeColumn(field='date_added', header='Date Added')
	date_modified = DatetimeColumn(field='date_modified', header='Date Modified')
	edit_link = LinkColumn(header='Edit', links=[Link(text='Edit', viewname='blog:edit_post', args=(A('uid'),)),])

	class Meta:
		model = Post
		pagination = True

