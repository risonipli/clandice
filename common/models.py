# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models

class AbstractMessage(models.Model):
	"""
	Абстрактный класс, представляющий сущность "сообщение". Основа всех
	последующих типов "сообщений"
	"""

	# заголовок сообщения
	title = models.CharField("Тема", max_length=30)
	# содержимое сообщения
	message = models.TextField("Тело сообщения")
	# автор сообщения. Ссылка на объект класса
	# django.contrib.auth.models.User
	created_by = models.ForeignKey(User,
			related_name="commons_abstractmessages_created_message")
	# время создания сообщения. Время фиксируется, когда объект создается
	created_on = models.DateTimeField("Время создания", auto_now_add=True)
	# поле-флаг проверяет удалено ли сообщение
	is_deleted = models.BooleanField("Удалено", default=False)
	# пользователь, который удалил сообщение. Ссылка на объект класса
	# django.contrib.auth.models.User
	deleted_by = models.ForeignKey(User,
			related_name="commons_abstractmessages_deleted_message",
			blank=True, null=True)
	# время удаления сообщения
	deleted_on = models.DateTimeField("Время удаления", auto_now=True)
	# ip-адрес пользователя, который создал сообщение
	ip_created_by = models.IPAddressField("IP-адрес пользователя, создавшего \
			сообщение", blank=True, null=True)
	# ip-адрес пользователя, который удалил сообщение
	ip_deleted_by = models.IPAddressField("IP-адрес пользователя, удалившего \
			сообщение", blank=True, null=True)
	# список пользователей, которые "прочитали" сообщение
	who_read = models.ManyToManyField(User,
			related_name="commons_abstractmessages_read_messages")

	class Meta:
		abstract = True

