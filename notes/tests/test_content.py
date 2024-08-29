import unittest

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from notes.models import Note
from notes.forms import NoteForm

User = get_user_model()


class TestNotesList(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Pony')
        cls.reader = User.objects.create(username='NotPony')
        cls.note = Note.objects.create(
            author=cls.author,
            title='Заголовок',
            text='Текст',
            slug='Slug'
        )

    @unittest.skip('Этот тест пропускаем')
    def test_notes_list_for_different_users(self):
        users_notes_list = (
            (self.author, True),
            (self.reader, False),
        )
        for user, status in users_notes_list:
            self.client.force_login(user)
            with self.subTest(user=user):
                url = reverse('notes:list')
                response = self.client.get(url)
                object_list = response.context['object_list']
                assert (self.note in object_list) is status

    @unittest.skip('Этот тест пропускаем')
    def test_create_note_page_contains_form(self):
        self.client.force_login(self.author)
        url = reverse('notes:add')
        response = self.client.get(url)
        assert 'form' in response.context
        assert isinstance(response.context['form'], NoteForm)

    def test_edit_note_page_contains_form(self):
        self.client.force_login(self.author)
        url = reverse('notes:edit', args=(self.note.slug,))
        response = self.client.get(url)
        assert 'form' in response.context
        assert isinstance(response.context['form'], NoteForm)
