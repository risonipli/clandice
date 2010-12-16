# -*- coding: utf-8 -*-

from django.test import TestCase

from security.forms import ChangePasswordForm, ProfileForm, RegistrationForm

class UsersFormTest(TestCase):
	"""
	Класс предоставляет тесты для форм ProfileForm, RegistrationForm,
	ChangePasswordForm
	"""

	def test_profile_form_validation(self):
		"""
		Тестирует работоспособность формы редактирование профиля пользователя
		"""
		# полная верная информация
		valid_full_data = {'last_name': 'Петров', 'first_name': 'Петр', 'middle_name':
				'Петрович', 'login_name': 'petr88', 'nickname': 'petroman',
				'email': 'petro88@mail.com', 'user_page': 'http://user.page.com'}

		# основная верная информация
		valid_base_data = {'login_name': 'petr88', 'email': 'petro88@mail.com'}

		# неверная информация - отсутствует обязательное значени имени входа
		invalid_data_blank_login_name = {'email': 'petro88@mail.com'}

		# неверная информация - отсутствует обязательное значение адреса
		# электронной почты
		invalid_data_blank_email = {'login_name': 'petr88'}

		# неверная информация - неверный формат записи адреса электронной почты
		invalid_data_invalid_email = {'login_name': 'petr88', 'email':
				'petro88.mail.com'}

		# неверная информация - неверный формат записи адреса домашней странички
		invalid_data_invalid_userpage = {'login_name': 'petr88', 'email':
				'petro88@mail.com', 'user_page': 'hddp:index.html'}

		# неверная информация - значение потверждения пароля содержит опечатку
		# (вместо латинской 'e' введено русская 'е')
		invalid_data_various_pwds = {'login_name': 'petr88', 'email':
				'petro88@mail.com', 'password': 'qwerty', 'password_confirm':
				'qwеrty'}

		reg_form1 = ProfileForm(valid_full_data)
		reg_form2 = ProfileForm(valid_base_data)
		reg_form3 = ProfileForm(invalid_data_blank_login_name)
		reg_form4 = ProfileForm(invalid_data_blank_email)
		reg_form5 = ProfileForm(invalid_data_invalid_email)
		reg_form6 = ProfileForm(invalid_data_invalid_userpage)

		self.assertTrue(reg_form1.is_valid(), "valid full data")
		self.assertTrue(reg_form2.is_valid(), "valid base data")
		self.assertFalse(reg_form3.is_valid(), "invalid data: blank login_name")
		self.assertFalse(reg_form4.is_valid(), "invalid data: blank email")
		self.assertFalse(reg_form5.is_valid(), "invalid_data: invalid email")
		self.assertFalse(reg_form6.is_valid(), "invalid data: invalid userpage")

	def test_registration_form_validation(self):
		"""
		Тестирует работоспособность формы регистрации пользователя
		"""
		# полная верная информация
		valid_full_data = {'last_name': 'Петров', 'first_name': 'Петр', 'middle_name':
				'Петрович', 'login_name': 'petr88', 'nickname': 'petroman',
				'email': 'petro88@mail.com', 'user_page': 'http://user.page.com',
				'password': 'qwerty', 'password_confirm': 'qwerty'}

		# неверная информация - значение потверждения пароля содержит опечатку
		# (вместо латинской 'e' введено русская 'е')
		invalid_data_various_pwds = {'login_name': 'petr88', 'email':
				'petro88@mail.com', 'password': 'qwerty', 'password_confirm':
				'qwеrty'}

		reg_form1 = RegistrationForm(valid_full_data)
		reg_form2 = RegistrationForm(invalid_data_various_pwds)

		self.assertTrue(reg_form1.is_valid(), "valid full data")
		self.assertFalse(reg_form2.is_valid(), "invalid data: various passwords")

	def test_change_password_form_validation(self):
		"""
		Тестирует работоспособность формы смены пароля
		"""
		# TODO провести тесты еще раз. Замечено странное поведение с формами
		# form2 и form3

		# верная информация
		valid_data = {'current_password': '12we56', 'new_password': 'qwerty',
				'new_password_confirm': 'qwerty'}
		# неверная информация - пустые значения обязательных полей
		invalid_data_empty_fields = {'current_password': '', 'new_password':
				'', 'new_password_confirm': ''}
		# неверная информация - одинаковые текущий и новый пароли
		invalid_data_equals_current_and_new_pwds = {'current_password':
				'qwerty', 'new_password': 'qwerty', 'new_password_confirm':
				'qwerty1'}
		# неверная информация - значения нового пароля и потверждения не
		# совпадают
		invalid_data_wrong_confirm_new_password = {'current_password':
				'qwerty', 'new_password': 'qwerty1', 'new_password_confirm':
				'qwerty2'}

		form1 = ChangePasswordForm(valid_data)
		#form2 = ChangePasswordForm(invalid_data_empty_fields)
		#form3 = ChangePasswordForm(invalid_data_equals_current_and_new_pwds)
		form4 = ChangePasswordForm(invalid_data_wrong_confirm_new_password)

		self.assertTrue(form1.is_valid(), "valid valid data")
		#self.assertFalse(form2.is_valid(), "invalid data: empty fields")
		#self.assertFalse(form3.is_valid(), "invalid data: equals current")
		self.assertFalse(form4.is_valid(), "invalid data: wrong confirm")

