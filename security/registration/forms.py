# -*- coding: utf-8 -*-
from django import forms

from security.profile.forms import ProfileForm

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

class SendInviteForm(forms.Form):
	email = forms.EmailField(label = 'E-mail, на который будет выслано приглашение')