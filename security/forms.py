# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User

class ProfileForm(forms.Form):
	"""
	Класс представляет собой форму для сбора данных о пользователе
	"""
	# фамилия пользователя
	last_name = forms.CharField(label="Фамилия:", max_length=30,
			required=False)
	# имя пользователя
	first_name = forms.CharField(label="Имя:", max_length=30, required=False)
	# отчество пользователя
	middle_name = forms.CharField(label = "Отчество:", max_length=30,
			required=False)
	# имя пользователя для входа в систему.
	# Это имя будет запрашиваться на форме аутентификации
	login_name = forms.CharField(label="Имя входа:", max_length=30)
	# "никнейм" пользователя. Это имя будет использоваться на сайте (будут
	# видеть другие пользователи)
	nickname = forms.CharField(label="Никнейм:", max_length=30, required=False)
	# адрес электронной почты регистрируемого пользователя
	email = forms.EmailField(label="Адрес электронной почты:")
	# адрес "домашней странички" пользователя
	user_page = forms.URLField(label="Домашняя страничка:", required=False)
	# "аватар" пользователя
	avatar = forms.ImageField(label="Аватар:", required=False)
	
	def clean_login_name(self):
		"""
		Проверяет на существование в системе пользователя с таким же именем
		входа. Если введеное значение имени еще не занято, то возвращается
		введенное значение, иначе - ошибка с сообщением, что такое имя уже
		существует
		"""
		# получаем введенное значение
		input_login_name = self.cleaned_data['login_name']
		# если введенное значение совпадает с текущим, то его и возвращаем
		#if self.login_name == input_login_name:
			#return login_name

		# ищем, есть ли пользователи с таким (введенным) именем
		try:
			User.objects.get(username=input_login_name)
			raise forms.ValidationError("Данное имя уже используется.\
					Пожалуйста, замените на другое")
		except User.DoesNotExist:
			# если пользователя не нашлось
			pass

		return input_login_name

class RegistrationForm(ProfileForm):
	"""
	Класс представляет собой форму регистрации пользователя
	"""

	# пароль регистрируемого пользователя
	password = forms.CharField(label="Пароль:", min_length=6, max_length=25,
			widget=forms.PasswordInput())
	# поле для проверки введенного пароля. Под проверкой здесь понимается
	# проверка на возможность случайной опечатки при вводе пароля
	password_confirm = forms.CharField(label="Потверждение пароля:",
			min_length=6, max_length=25, widget=forms.PasswordInput())

	def clean_password_confirm(self):
		"""
		Проверяет введенный пароль на возможность случайной опечатки при вводе
		"""
		pwd = self.cleaned_data['password_confirm']
		if self.cleaned_data['password'] != pwd:
			raise forms.ValidationError("Пароль и потверждение пароля не\
					совпадают!")

		return pwd

class ChangePasswordForm(forms.Form):
	"""
	Класс представляет собой форму для смены текущего пароля на новый
	"""

	# текущий пароль пользователя
	current_password = forms.CharField(label="Текущий пароль:", min_length=6,
			max_length=25, widget=forms.PasswordInput())
	# новый пароль пользователя
	new_password = forms.CharField(label="Новый пароль:", min_length=6,
			max_length=25, widget=forms.PasswordInput())
	# проверка на возможность случайной опечатки при вводе нового пароля
	new_password_confirm = forms.CharField(label="Потверждение нового пароля:",
			min_length=6, max_length=25, widget=forms.PasswordInput())

	def clean_new_password(self):
		"""
		Проверяет новый пароль на "непохожесть" на текущий. Если новый пароль
		идентичен текущему выбрасывается исключение
		"""
		pwd = self.cleaned_data['new_password']
		if self.cleaned_data['current_password'] == pwd:
			raise forms.ValidationError("Новый пароль идентичен текущему.\
					Проверьте корректность ввода")

		return pwd

	def clean_new_password_confirm(self):
		"""
		Проверяет новый пароль на возможность случайной опечатки при вводе
		"""
		pwd = self.cleaned_data['new_password_confirm']
		if self.cleaned_data['new_password'] != pwd:
			raise forms.ValidationError("Пароль и потверждение пароля не\
					совпадают!")

		return pwd

