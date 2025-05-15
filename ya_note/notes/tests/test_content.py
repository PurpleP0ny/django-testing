from notes.forms import NoteForm
from notes.models import Note

from .common import ADD_URL, EDIT_URL, LIST_URL, TestCaseWithData


class TestPagesNote(TestCaseWithData):
    def test_note_in_list_for_author(self):
        """Заметка передаётся на страницу со списком заметок."""
        response = self.author_client.get(LIST_URL)
        response.context['object_list']
        self.assertEqual(Note.objects.count(), 1)
        notes = Note.objects.get()
        self.assertEqual(notes.text, self.note.text)
        self.assertEqual(notes.author, self.note.author)
        self.assertEqual(notes.title, self.note.title)
        self.assertEqual(notes.slug, self.note.slug)

    def test_note_not_in_list_for_another_user(self):
        """В список заметок одного пользователя не попадают заметки другого."""
        response = self.auth_client.get(LIST_URL)
        object_list = response.context['object_list']
        self.assertEqual(object_list.count(), 0)

    def test_pages_contains_form(self):
        """На страницы создания и редактирования заметки передаются формы."""
        urls = (ADD_URL, EDIT_URL)
        for url in urls:
            with self.subTest(name=url):
                response = self.author_client.get(url)
                form = response.context.get('form')
                self.assertIsInstance(form, NoteForm)
