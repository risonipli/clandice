# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from security.profile.forms import ProfileForm

class RegistrationForm(ProfileForm):
	"""
	Класс представляет собой форму регистрации пользователя
	"""
	# имя используемое пользователем для входа на сайт, уникален в системе,
	# не предоставлять возможность изменения
	login_name = forms.CharField(label='Имя входа', max_length=20)
	# адрес электронной почти пользователя, используется для получения
	# пользователем уведомлений и восстановления пароля, уникален в системе,
	# не предоставлять возможность смены
	email = forms.EmailField(label='E-mail')
	# псевдоним пользователя, используется для именования пользователя на сайте,
	# предоставить возможность изменения, уникален в системе
	nickname = forms.CharField(label='Никнейм', max_length=20)
	# пароль регистрируемого пользователя
	password = forms.CharField(label="Пароль:", min_length=6, max_length=25,
			widget=forms.PasswordInput())
	# поле для проверки введенного пароля. Под проверкой здесь понимается
	# проверка на возможность случайной опечатки при вводе пароля
	password_confirm = forms.CharField(label="Потверждение пароля:",
			min_length=6, max_length=25, widget=forms.PasswordInput())

	def clean_password_confirm(self):
		"""
		проверяет совпадают ли задаваемый пользователем пароль, и его подтверждение,
		в случае когда пароли не совпадают, возвращает сообщение о ошибке
		"""
		pwd = self.cleaned_data['password_confirm']
		if self.cleaned_data['password'] != pwd:
			raise forms.ValidationError("Пароль и потверждение пароля не\
					совпадают!")
		return pwd

	def clean_login_name(self):
		"""
		проверяет задаваемое пользователем имя входа в систему, в случае, когда
		данное имя уже зарегестрировано, возвращает сообщение о ошибке
		"""
		login_name = self.cleaned_data['login_name']
		try:
			User.objects.get(username=login_name)
			raise forms.ValidationError('Данное имя входа уже используется.')
		except User.DoesNotExist:
			return login_name

	def clean_email(self):
		"""
		проверяет задаваемый пользователем адрес электронной почты, в случае,
		когда данный адрес уже зарегестрирован, возвращает сообщение о ошибке
		"""
		email = self.cleaned_data['email']
		try:
			User.objects.get(email=email)
			raise forms.ValidationError('Данный email уже используется.')
		except User.DoesNotExist:
			return email

class InviteForm(forms.Form):
	"""
	Реализует форму рассылки приглашений - зарегистрироваться на ресурсе.
	Содержит единственное поле - адрес электронной почты, на который высылается
	письмо содержащее сгенерированную ссылку ведущую на форму регистрации.
	Приглашения могут рассылать пользователи обладающие соответствующим правом.
	"""
	email = forms.EmailField(label = 'E-mail, на который будет выслано приглашение')