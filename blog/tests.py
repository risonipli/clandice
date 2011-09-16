# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.test import TestCase

from blog.forms import CommentForm, PostForm
from blog.models import Post

class PostTest(TestCase):

	def test_create_post(self):
		"""
		"""
		# пользователь раз
		user1 = User.objects.create_user("user1", "user1@mail.com",
				"user1pwd")
		# пользователь два
		user2 = User.objects.create_user("user2", "user2@mail.com",
				"user2pwd")
		# пользователь три
		user3 = User.objects.create_user("user3", "user3@mail.com",
				"user3pwd")

		# создаем корень "дерева"
		# FIXME корень не должен создавать пользователь!
		root = Post.add_root(title="root title", message="root message",
				created_by=user1)
		self.assertNotEquals(root, None)

		# второй пользователь создал пост
		node0 = root.add_child(title="node0 title",
				message="node0d message", created_by=user2)
		# третий пользователь прочитал пост
		node0.who_read.add(user3)
		self.assertNotEquals(node0, None)

		# третий пользователь создал пост
		node1 = node0.add_sibling(title="node1 title", message="node1 message",
				created_by=user3)
		# первый пользователь прочитал пост
		node1.who_read.add(user1)
		self.assertNotEquals(node1, None)

		# первый пользователь создал комментарий к посту №1
		node2 = node1.add_child(title="node2 comment for node1 title",
				message="node2 comment for node1 message",
				created_by=user1)
		# второй пользователь прочитал пост №1
		node1.who_read.add(user2)
		# второй пользователь прочитал комментарий первого пользователя
		node2.who_read.add(user2)
		self.assertNotEquals(node2, None)

		# второй пользователь создал комментарий к посту №1
		node3 = node2.add_sibling(title="node3 comment for node1 title",
				message="node3 comment for node1 message",
				created_by=user2)
		self.assertNotEquals(node3, None)

		# третий пользователь откомментировал комментарий первого
		# пользователя
		node4 = node2.add_child(title="node4 comment for node2 title",
				message="node4 comment for node2 message",
				created_by=user3)
		self.assertNotEquals(node4, None)

class PostFormsTest(TestCase):

	def test_comment_form(self):
		"""
		Проверяет работоспособность формы комментирования сообщения
		"""
		valid_data = {"message": "message"}
		invalid_data = {"message": ""}

		form_with_valid_data = CommentForm(valid_data)
		self.assertTrue(form_with_valid_data.is_valid())

		form_with_invalid_data = CommentForm(invalid_data)
		self.assertFalse(form_with_invalid_data.is_valid())


	def test_post_form(self):
		"""
		Проверяет работоспособность формы создания сообщения
		"""
		valid_data = {"title": "Message Title", "message": "Message",
				"public": "Да"}
		invalid_data_empty_title = {"title": "", "message": "Message",
				"public": "Нет"}
		invalid_data_empty_message = {"title": "Message Title", "message": "",
				"public": "Да"}
		invalid_data_wrong_public_value = {"title": "Message Title",
				"message": "Message", "public": "z"}

		form_with_valid_data = PostForm(valid_data)
		form_witn_invalid_data_empty_title = PostForm(invalid_data_empty_title)
		form_with_invalid_data_empty_message = PostForm(invalid_data_empty_message)
		form_with_invalid_data_wrong_public_value = PostForm(invalid_data_wrong_public_value)

		self.assertTrue(form_with_valid_data.is_valid())
		self.assertFalse(form_witn_invalid_data_empty_title.is_valid())
		self.assertFalse(form_with_invalid_data_empty_message.is_valid())
		self.assertFalse(form_with_invalid_data_wrong_public_value.is_valid())

