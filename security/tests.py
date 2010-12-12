# -*- coding: utf-8 -*-

from django.test import TestCase

from security.forms import RegistrationForm

class RegistrationFormTest(TestCase):

	def test_form_validation(self):
		"""
		Тестирует работоспособность формы регистрации пользователя
		"""
		# полная верная информация
		valid_full_data = {'last_name': 'Петров', 'first_name': 'Петр', 'middle_name':
				'Петрович', 'login_name': 'petr88', 'nickname': 'petroman',
				'email': 'petro88@mail.com', 'password':
				'qwerty', 'password_confirm': 'qwerty'}

		# основная верная информация
		valid_base_data = {'login_name': 'petr88', 'email': 'petro88@mail.com',
				'password': 'qwerty', 'password_confirm': 'qwerty'}

		# неверная информация - отсутствует обязательное значени имени входа
		invalid_data_blank_login_name = {'email': 'petro88@mail.com',
				'password': 'qwerty', 'password_confirm': 'qwerty'}

		# неверная информация - отсутствует обязательное значение адреса
		# электронной почты
		invalid_data_blank_email = {'login_name': 'petr88', 'password':
				'qwerty', 'password_confirm': 'qwerty'}

		# неверная информация - неверное значение адреса электронной почты
		invalid_data_invalid_email = {'login_name': 'petr88', 'email':
				'petro88.mail.com', 'password': 'qwerty', 'password_confirm':
				'qwerty'}

		# неверная информация - значение потверждения пароля содержит опечатку
		# (вместо латинской 'e' введено русская 'е')
		invalid_data_various_pwds = {'login_name': 'petr88', 'email':
				'petro88@mail.com', 'password': 'qwerty', 'password_confirm':
				'qwеrty'}

		reg_form1 = RegistrationForm(valid_full_data)
		reg_form2 = RegistrationForm(valid_base_data)
		reg_form3 = RegistrationForm(invalid_data_blank_login_name)
		reg_form4 = RegistrationForm(invalid_data_blank_email)
		reg_form5 = RegistrationForm(invalid_data_invalid_email)
		reg_form6 = RegistrationForm(invalid_data_various_pwds)

		self.assertTrue(reg_form1.is_valid(), "valid full data")
		self.assertTrue(reg_form2.is_valid(), "valid base data")
		self.assertFalse(reg_form3.is_valid(), "invalid data: blank login_name")
		self.assertFalse(reg_form4.is_valid(), "invalid data: blank email")
		self.assertFalse(reg_form5.is_valid(), "invalid_data: invalid email")
		self.assertFalse(reg_form6.is_valid(), "invalid data: various pwds")

