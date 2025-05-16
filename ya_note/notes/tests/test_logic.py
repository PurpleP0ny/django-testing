from http import HTTPStatus

from pytils.translit import slugify

from notes.models import Note

from .common import (ADD_URL, DELETE_URL, EDIT_URL, SUCCESS_URL,
                     TestCaseWithData)


class TestNotesCreation(TestCaseWithData):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.form_data = {
            'title': 'Новый заголовок',
            'text': 'Новый текст',
            'slug': 'test-slug',
        }
        cls.form_data_empty_slug = {
            'title': 'Заголовок без slug',
            'text': 'Текст без slug',
        }
        cls.form_data_duplicate_slug = {
            'title': 'Другой заголовок',
            'text': 'Другой текст',
            'slug': 'test-slug',
        }

    def test_user_can_create_note(self):
        """Залогиненный пользователь может создать заметку."""
        Note.objects.all().delete()
        response = self.auth_client.post(ADD_URL, data=self.form_data)
        self.assertRedirects(response, SUCCESS_URL)
        self.assertEqual(Note.objects.count(), 1)
        note = Note.objects.first()
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.slug, self.form_data['slug'])
        self.assertEqual(note.author, self.user)

    def test_not_unique_slug(self):
        """Невозможно создать две заметки с одинаковым slug."""
        self.auth_client.post(ADD_URL, data=self.form_data)
        initial_count = Note.objects.count()
        response = self.auth_client.post(
            ADD_URL,
            data=self.form_data_duplicate_slug
        )
        self.assertEqual(Note.objects.count(), initial_count)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_empty_slug(self):
        """Если slug не указан, он генерируется автоматически."""
        Note.objects.all().delete()
        response = self.auth_client.post(
            ADD_URL,
            data=self.form_data_empty_slug
        )
        self.assertRedirects(response, SUCCESS_URL)
        note = Note.objects.first()
        expected_slug = slugify(self.form_data_empty_slug['title'])
        self.assertEqual(note.slug, expected_slug)
        self.assertEqual(note.title, self.form_data_empty_slug['title'])
        self.assertEqual(note.text, self.form_data_empty_slug['text'])


class TestNoteEditDelete(TestCaseWithData):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.form_data = {
            'title': 'Обновленный заголовок',
            'text': 'Обновленный текст',
            'slug': 'updated-slug',
        }

    def test_author_can_delete_note(self):
        """Автор может удалить свою заметку."""
        initial_count = Note.objects.count()
        response = self.author_client.delete(DELETE_URL)
        self.assertRedirects(response, SUCCESS_URL)
        self.assertEqual(Note.objects.count(), initial_count - 1)

    def test_user_cant_delete_note_of_another_user(self):
        """Пользователь не может удалить чужую заметку."""
        initial_count = Note.objects.count()
        response = self.reader_client.delete(DELETE_URL)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(Note.objects.count(), initial_count)

    def test_author_can_edit_notes(self):
        """Автор может редактировать свою заметку."""
        response = self.author_client.post(EDIT_URL, data=self.form_data)
        self.assertRedirects(response, SUCCESS_URL)
        note = Note.objects.get(pk=self.note.pk)
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.slug, self.form_data['slug'])

    def test_user_cant_edit_note_of_another_user(self):
        """Пользователь не может редактировать чужую заметку."""
        initial_note = Note.objects.get(pk=self.note.pk)
        response = self.reader_client.post(EDIT_URL, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        updated_note = Note.objects.get(pk=self.note.pk)
        self.assertEqual(initial_note.title, updated_note.title)
        self.assertEqual(initial_note.text, updated_note.text)
        self.assertEqual(initial_note.slug, updated_note.slug)
