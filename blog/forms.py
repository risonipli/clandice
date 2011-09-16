# -*- coding: utf-8 -*-

from django import forms

class CommentForm(forms.Form):
	"""
	Класс представляет собой форму для ввода текста сообщения
	"""
	message = forms.CharField(label="Текст сообщения", widget=forms.Textarea)

	def clean_message(self):
		"""
		Проверяет, что введеное собщение не пусто
		"""
		input_message = self.cleaned_data['message']
		if len(input_message) == 0:
			raise forms.ValidationError("Сообщение не может быть пустым")
		else:
			return input_message

# варианты публикации сообщения: сообщение будет видно или всем пользователям
# или только зарегистрированым
DISPLAY_CHOICES = (
		("Да", "y"),
		("Нет", "n"),
)

class PostForm(CommentForm):
	"""
	Класс представляет собой форму для ввода поста
	"""
	title = forms.CharField(label="Тема", max_length=30)
	public = forms.ChoiceField(label="Виден всем?", choices=DISPLAY_CHOICES)

	def clean_title(self):
		"""
		Проверяет, что заголовок сообщения не пуст
		"""
		input_title = self.cleaned_data['title']
		if len(input_title) == 0:
			raise forms.ValidationError("Заголовок сообщения не может быть пустым")
		else:
			return input_title

