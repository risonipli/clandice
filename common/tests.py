# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.test import TestCase

class UserTest(TestCase):

	def test_user_creation(self):
		"""
		Тестирует создание пользователей и дополнительной информации о
		пользователях
		"""
		user1 = User.objects.create_user("user1", "user1@mail.com", "user1pwd")
		user1.last_name = "User1_LN"
		user1.first_name = "User1_FN"
		user1.save()

		user2 = User.objects.create_user("user2", "user2@mail.com", "user2pwd")
		user2.last_name = "User2_LN"
		user2.first_name = "User2_FN"
		user2.save()

		print user1
		print user2
		print user1.get_profile()
		print user2.get_profile()

