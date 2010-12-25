# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.test import TestCase

from common.models import AbstractMessage

class MessageTest(TestCase):

	def test_abstract_message(self):
		"""
		"""
		user = User.objects.create_user("user", "user@mail.com", "userpwd")
		message = AbstractMessage(title="заголовок", message="тело сообщения",
				created_by=user, deleted_by=user)
		#self.assertRaises(Exception, message.save())
		#try:
		#	message.save()
		#except Exception:
		#	pass
		#else:
		#	self.asserTrue(1 == 2)
		#	print "wtf?!"

