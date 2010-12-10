# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

class UserInfo(models.Model):
	"""
	Класс предоставляет дополнительную информацию о пользователе, помимо той,
	что предоставлена в классе django.contrib.auth.models.User
	"""

	# ссылка на объект класса django.contrib.auth.models.User
	user = models.ForeignKey(User, unique=True)
	# отчество пользователя
	middle_name = models.CharField("Отчество", blank=True, max_length=30,
			null=True)
	# "никнейм" пользователя. Никнейм используется на сайте, когда как username
	# только при входе в систему
	nickname = models.CharField("Никнейм", blank=True, db_index=True,
			max_length=30, unique=True)
	# дата блокирования пользователя (запрета пользователя входить в систему)
	blocked_after = models.DateTimeField("Блокирован после", blank=True,
			null=True)
	# дата разблокирования пользователя (разрешение пользователю входить в
	# систему)
	blocked_until = models.DateTimeField("Блокирован до", blank=True,
			null=True)
	# ip-адрес пользователя, с которого он в последний раз заходил в систему.
	# Обновляется с каждым входом пользователя в систему
	ip = models.IPAddressField("IP-адрес", blank=True, null=True)
	# адрес "домашней странички" пользователя. Это может быть к примеру ссылка
	# на блог, страницу социальной сети и тому подобное
	user_page = models.URLField("Домашняя страничка", blank=True, null=True)
	# поле позволяет проверить на уровне шаблона есть ли у пользователя
	# "аватар"
	has_avatar = models.BooleanField("Есть ли аватар?", default=False)

	class Admin:
		list_display = ("middle_name", "nickname", "blocked_after",
				"blocked_until", "ip", "user_page", "has_avatar",)
		ordering = ("nickname",)

	class Meta:
		ordering = ["nickname"]

	def __unicode__(self):
		return '{0} "{1}" {2}'.format(self.user.last_name, self.nickname,
				self.user.first_name)

def create_user_profile(sender, instance, created, **kwargs):
	"""
	Сохраняет дополнительную информацию о пользователе
	"""
	if created:
		profile, created = UserInfo.objects.get_or_create(user=instance,
				nickname=instance.username)

# регистрируем функцию сохранения дополнительной информации о пользователе.
# После сохранения данных о пользователе (User.objects.create_user)
# посылается сигнал о сохранении дополнительной информации
post_save.connect(create_user_profile, sender=User)

