import pytest
from http import HTTPStatus


@pytest.mark.django_db
def test_home_page_availability(anonymous_client, home_url):
    response = anonymous_client.get(home_url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_news_detail_availability(anonymous_client, detail_url):
    response = anonymous_client.get(detail_url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_comment_edit_delete_availability_for_author(author_client,
                                                     edit_url, delete_url):
    for url in (edit_url, delete_url):
        response = author_client.get(url)
        assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_redirect_anonymous_to_login(anonymous_client, edit_url,
                                     delete_url, login_url):
    for url in (edit_url, delete_url):
        response = anonymous_client.get(url)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == f"{login_url}?next={url}"


@pytest.mark.django_db
def test_comment_edit_delete_unavailable_for_reader(reader_client,
                                                    edit_url, delete_url):
    for url in (edit_url, delete_url):
        response = reader_client.get(url)
        assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
def test_auth_pages_availability(anonymous_client,
                                 login_url, signup_url, logout_url):
    # Проверяем только login и signup
    for url in (login_url, signup_url):
        response = anonymous_client.get(url)
        assert response.status_code == HTTPStatus.OK
