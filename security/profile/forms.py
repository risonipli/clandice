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

