# -*- coding: utf-8 -*-

from django.db import models

class Invite(models.Model):
	key = models.CharField(max_length=32, unique=True)
	email = models.EmailField()

	class Admin:
		list_display = ('key', 'email')

	def __unicode__(self):
		return self.key

