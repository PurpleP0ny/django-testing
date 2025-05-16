from http import HTTPStatus

import pytest
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment
from .constants import COMMENT_FORM_DATA

pytestmark = pytest.mark.django_db


def test_anonymous_user_cant_create_comment(anonymous_client, detail_url,
                                            login_url):
    initial_count = Comment.objects.count()
    response = anonymous_client.post(detail_url, data=COMMENT_FORM_DATA)
    assertRedirects(response, f'{login_url}?next={detail_url}')
    assert Comment.objects.count() == initial_count


def test_user_can_create_comment(author_client, detail_url,
                                 author, news):
    Comment.objects.all().delete()
    response = author_client.post(detail_url, data=COMMENT_FORM_DATA)
    assertRedirects(response, f'{detail_url}#comments')
    assert Comment.objects.count() == 1
    comment = Comment.objects.first()
    assert comment.text == COMMENT_FORM_DATA['text']
    assert comment.news == news
    assert comment.author == author


@pytest.mark.parametrize('bad_word', BAD_WORDS)
def test_user_cant_use_bad_words(bad_word, author_client, detail_url):
    initial_count = Comment.objects.count()
    bad_comment_data = {'text': bad_word}
    response = author_client.post(detail_url, data=bad_comment_data)
    assertFormError(response.context['form'], 'text', WARNING)
    assert Comment.objects.count() == initial_count


def test_author_can_delete_comment(author_client,
                                   delete_url, detail_url):
    initial_count = Comment.objects.count()
    response = author_client.delete(delete_url)
    assertRedirects(response, f'{detail_url}#comments')
    assert Comment.objects.count() == initial_count - 1


def test_user_cant_delete_comment_of_another_user(reader_client, delete_url):
    initial_count = Comment.objects.count()
    response = reader_client.delete(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == initial_count


def test_author_can_edit_comment(author_client, edit_url, detail_url):
    new_text = 'Обновленный комментарий'
    response = author_client.post(edit_url, data={'text': new_text})
    assertRedirects(response, f"{detail_url}#comments")
    comment = Comment.objects.first()
    assert comment.text == new_text


def test_user_cant_edit_comment_of_another_user(reader_client, edit_url):
    original_text = Comment.objects.first().text
    response = reader_client.post(edit_url, data={'text': 'Новый текст'})
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment = Comment.objects.first()
    assert comment.text == original_text
