from table import Table
from table.columns import Column

from api.models import BlogComment, BlogCategory, Post

class PostTable(Table):
	'''
	table for blog posts
	'''

	uid = Column(field='uid')
	title = Column(field='title')
	image = Column(field='image')
	content = Column(field='content')
	url = Column(field='url')
	category = Column(field='category')
	date_added = Column(field='date_added')
	date_modified = Column(field='date_modified')

	class Meta:
		model = Post

