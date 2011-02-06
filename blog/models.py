# -*- coding: utf-8 -*-

from django.db import models

from treebeard.ns_tree import NS_Node

from common.models import AbstractMessage

class Post(AbstractMessage, NS_Node):
	"""
	Данный класс представляет собой сущности "пост" и "комментарии".
	Организует древовидную структуру данных
	"""

	# контент будет доступен всем пользователям или только
	# зарегистрированным
	is_public = models.BooleanField("Виден всем?", default=True)
	# ip-адрес пользователя, который изменил сообщение
	ip_change_by = models.IPAddressField("IP-адрес пользователя, \
			изменившего пост", blank=True, null=True)
	# node_order_by = ["created_on"]

	class Meta:
		ordering = ["tree_id", "lft"]

