# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.views.generic.edit import FormView

from blog.forms import PostForm
from blog.models import Post

class AddPostView(FormView):
	"""
	Класс предоставляет возможность пользователям создавать пост.
	"""

	template_name = "blog/add_post.html"

	def get_form_class(self):
		return PostForm

	def get_success_url(self):
		return "/"

	def form_valid(self, form):
		# получаем корневой элемент. Он будет выступать родителем для поста
		root_node = Post.get_first_root_node()
		if root_node is None:
			raise Exception("корневой элемент не существует")

		node_title = form.cleaned_data['title']
		node_message = form.cleaned_data['message']
		public = form.cleaned_data['public']
		if public == 'y':
			node_public = True
		elif public == 'n':
			node_public = False
		else:
			raise TypeError("неверный параметр параметра public")

		# создаем пост
		node = root_node.add_child(title=node_title, message=node_message,
				is_public=node_public, created_by=self.request.user)
		node.save()

		return super(AddPostView, self).form_valid(form)

	def form_invalid(self, form):
		return super(AddPostView, self).form_invalid(form)

