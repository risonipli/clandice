# -*- coding: utf-8 -*-

import os.path

import settings

from django.contrib.auth.models import User
from django.views.generic import DetailView
from django.views.generic.edit import FormView

from security.profile.forms import ProfileForm

class ProfileDisplayView(DetailView):
	"""
	Класс предоставляет возможность пользователю просматривать свой профиль.
	"""
	context_object_name = "person"
	template_name = "security/profile/profile_view.html"

	def get_object(self):
		try:
			return User.objects.get(id=int(self.kwargs['user_id']))
		except (TypeError, OverflowError, KeyError, User.DoesNotExist):
			return self.request.user

class ProfileEditView(FormView):
	"""
	Класс предоставляет возможность пользователю редактировать свой профиль.
	"""

	template_name = "security/profile/profile_edit.html"

	def get_initial(self):
		user = self.request.user
		user_profile = user.get_profile()
		data = {
				"last_name": user.last_name,
				"first_name": user.first_name,
				"middle_name": user_profile.middle_name,
				"login_name": user.username,
				"nickname": user_profile.nickname,
				"email": user.email,
				"user_page": user_profile.user_page
				}

		return data

	def get_form_class(self):
		return ProfileForm

	def get_form_kwargs(self):
		kwargs = super(FormView, self).get_form_kwargs()
		kwargs.update({"user": self.request.user})
		return kwargs

	def get_success_url(self):
		return "/profile/view/"

	def form_valid(self, form):
		user = self.request.user
		user.last_name = form.cleaned_data['last_name']
		user.first_name = form.cleaned_data['first_name']
		user.username = form.cleaned_data['login_name']
		user.email = form.cleaned_data['email']

		user_profile = user.get_profile()
		user_profile.middle_name = form.cleaned_data['middle_name']
		user_profile.nickname = form.cleaned_data['nickname']
		user_profile.user_page = form.cleaned_data['user_page']
		if 'avatar' in self.request.FILES.keys():
			avatar = self.request.FILES['avatar']
			self._save_avatar(avatar)
			user_profile.has_avatar = True

		user_profile.save()
		user.save()

		return super(ProfileEditView, self).form_valid(form)

	def form_invalid(self, form):
		return super(ProfileEditView, self).form_invalid(form)

	def _save_avatar(self, image_file):
		"""
		Сохраняет аватар пользователя.
		"""
		# строим путь до изображения на сервере
		avatar = os.path.join(settings.MEDIA_ROOT, 'avatars',
				str(self.request.user.id))
		# записываем данные в фаил
		with open(avatar, 'wb+') as f:
			for chunck in image_file.chunks():
				f.write(chunck)

