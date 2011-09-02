# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.views.generic import DetailView

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

