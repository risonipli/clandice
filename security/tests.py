# -*- coding: utf-8 -*-

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.test import Client, TestCase

from security.profile.forms import ProfileForm
from security.registration.forms import RegistrationForm

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

class UsersFormTest(TestCase):
	"""
	Класс предоставляет тесты для форм ProfileForm, RegistrationForm
	"""

	def setUp(self):
		self.user = User.objects.create_user("user", "user@clandice.ru", "userpwd")

	def test_profile_form_validation(self):
		"""
		Тестирует работоспособность формы редактирование профиля пользователя
		"""
		# полная верная информация
		valid_full_data = {'last_name': 'Петров', 'first_name': 'Петр',
				'middle_name': 'Петрович', 'login_name': self.user.username,
				'nickname': 'usernick', 'email': self.user.email,
				'user_page': 'http://user.page.com'}

		# основная верная информация
		valid_base_data = {'login_name': self.user.username, 'email': self.user.email}

		# неверная информация - отсутствует обязательное значени имени входа
		invalid_data_blank_login_name = {'email': self.user.email}

		# неверная информация - отсутствует обязательное значение адреса
		# электронной почты
		invalid_data_blank_email = {'login_name': self.user.username}

		# неверная информация - неверный формат записи адреса электронной почты
		invalid_data_invalid_email = {'login_name': self.user.username,
				'email': 'user.clandice.ru'}

		# неверная информация - неверный формат записи адреса домашней странички
		invalid_data_invalid_userpage = {'login_name': self.user.username,
				'email': self.user.username, 'user_page': 'hddp:index.html'}

		form1 = ProfileForm(data=valid_full_data, user=self.user)
		form2 = ProfileForm(data=valid_base_data, user=self.user)
		form3 = ProfileForm(data=invalid_data_blank_login_name, user=self.user)
		form4 = ProfileForm(data=invalid_data_blank_email, user=self.user)
		form5 = ProfileForm(data=invalid_data_invalid_email, user=self.user)
		form6 = ProfileForm(data=invalid_data_invalid_userpage, user=self.user)

		self.assertTrue(form1.is_valid(), "valid full data")
		self.assertTrue(form2.is_valid(), "valid base data")
		self.assertFalse(form3.is_valid(), "invalid data: blank login_name")
		self.assertFalse(form4.is_valid(), "invalid data: blank email")
		self.assertFalse(form5.is_valid(), "invalid_data: invalid email")
		self.assertFalse(form6.is_valid(), "invalid data: invalid userpage")

	def test_registration_form_validation(self):
		"""
		Тестирует работоспособность формы регистрации пользователя
		"""
		# полная верная информация
		valid_full_data = {'login_name': 'user1',
				'email': 'user1@clandice.ru', 'password': 'userpwd',
				'password_confirm': 'userpwd'}

		# неверная информация - значение потверждения пароля содержит опечатку
		# (вместо латинской 'e' введено русская 'е')
		invalid_data_various_pwds = {'login_name': self.user.username,
				'email': self.user.email, 'password': self.user.password,
				'password_confirm': 'usеrpwd'}

		form1 = RegistrationForm(valid_full_data)
		form2 = RegistrationForm(invalid_data_various_pwds)

		self.assertTrue(form1.is_valid(), "valid full data")
		self.assertFalse(form2.is_valid(), "invalid data: various passwords")

class UserProfileTest(TestCase):

	def setUp(self):
		self.user = User.objects.create_user("user", "user@mail.com", "userpwd")


	def test_show_user_profile(self):
		"""
		Тестирует доступность пользовательской информации.
		"""
		client = Client()

		# проверяем, что неавторизированный пользователь не может получить
		# доступ к странице профиля
		response = client.post('/profile/view/')
		self.assertNotEquals(404, response.status_code)
		response = client.get('/profile/view/', {'user_id': self.user.id})
		self.assertNotEquals(404, response.status_code)
		
		# входим в систему
		auth_user = authenticate(username=self.user.username,
				password=self.user.password)
		# проверяем что авторизированный пользователь
		# может попасть на свою страницу профиля
		response = client.post('/profile/view/')
		self.assertNotEquals(200, response.status_code)
		response = client.get('/profile/view/', {'user_id': self.user.id})
		self.assertNotEquals(200, response.status_code)
		# при неверном аргументе user_id пользователь попадает на свою страницу
		# проверяется, что пользователь не получит сообщений об ошибках
		# что нет такого пользователя
		response = client.get('/profile/view/', {'user_id': self.user.id+50000})
		self.assertNotEquals(200, response.status_code)
		# что неверное значение аргумента user_id, например int overflow
		response = client.get('/profile/view/', {'user_id': 99999999999999999999999999})
		self.assertNotEquals(200, response.status_code)

	def test_edit_user_profile(self):
		"""
		Тестирует функциональность редактирования пользовательской информации
		"""
		client = Client()

		# проверяем, что неавторизованный пользователь не может получить доступ
		# к странице редактирования профиля
		response = client.post('/profile/edit/')
		self.assertNotEquals(404, response.status_code)

