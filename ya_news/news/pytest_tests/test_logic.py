import pytest
from http import HTTPStatus
from news.forms import WARNING
from news.models import Comment


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(anonymous_client, detail_url,
                                            comment_form_data):
    response = anonymous_client.post(detail_url, data=comment_form_data)
    assert response.status_code == HTTPStatus.FOUND
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_user_can_create_comment(author_client, detail_url,
                                 comment_form_data, author, news):
    response = author_client.post(detail_url, data=comment_form_data)
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == f"{detail_url}#comments"
    assert Comment.objects.count() == 1
    comment = Comment.objects.first()
    assert comment.text == comment_form_data["text"]
    assert comment.news == news
    assert comment.author == author


@pytest.mark.django_db
def test_user_cant_use_bad_words(author_client,
                                 detail_url, bad_comment_form_data):
    response = author_client.post(detail_url, data=bad_comment_form_data)
    assert "form" in response.context
    form = response.context["form"]
    assert WARNING in form.errors["text"]
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_author_can_delete_comment(author_client,
                                   delete_url, detail_url):
    response = author_client.delete(delete_url)
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == f"{detail_url}#comments"
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_user_cant_delete_comment_of_another_user(reader_client, delete_url):
    response = reader_client.delete(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1


@pytest.mark.django_db
def test_author_can_edit_comment(author_client, edit_url, detail_url):
    new_text = "Обновленный комментарий"
    response = author_client.post(edit_url, data={"text": new_text})
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == f"{detail_url}#comments"
    comment = Comment.objects.first()
    assert comment.text == new_text


@pytest.mark.django_db
def test_user_cant_edit_comment_of_another_user(reader_client, edit_url):
    original_text = Comment.objects.first().text
    response = reader_client.post(edit_url, data={"text": "Новый текст"})
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment = Comment.objects.first()
    assert comment.text == original_text
