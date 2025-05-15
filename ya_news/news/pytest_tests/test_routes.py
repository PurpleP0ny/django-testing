from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'url_name, client_fixture, expected_status',
    [
        ('news:home', 'anonymous_client', HTTPStatus.OK),
        ('news:detail', 'anonymous_client', HTTPStatus.OK),
        ('users:login', 'anonymous_client', HTTPStatus.OK),
        ('users:signup', 'anonymous_client', HTTPStatus.OK),
    ],
    ids=[
        'home_page_available',
        'news_detail_available',
        'login_page_available',
        'signup_page_available'
    ]
)
def test_pages_availability(request, url_name, client_fixture,
                            expected_status, news):
    client = request.getfixturevalue(client_fixture)
    url = reverse(url_name,
                  args=(news.id,) if url_name == 'news:detail' else None)
    response = client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url_name, client_fixture, expected_status, redirect_url',
    [
        ('news:edit', 'anonymous_client', HTTPStatus.FOUND, 'users:login'),
        ('news:delete', 'anonymous_client', HTTPStatus.FOUND, 'users:login'),
        ('news:edit', 'reader_client', HTTPStatus.NOT_FOUND, None),
        ('news:delete', 'reader_client', HTTPStatus.NOT_FOUND, None),
        ('news:edit', 'author_client', HTTPStatus.OK, None),
        ('news:delete', 'author_client', HTTPStatus.OK, None),
    ],
    ids=[
        'anon_edit_redirect',
        'anon_delete_redirect',
        'reader_edit_not_found',
        'reader_delete_not_found',
        'author_edit_ok',
        'author_delete_ok'
    ]
)
def test_comment_actions_availability(
    request,
    url_name,
    client_fixture,
    expected_status,
    redirect_url,
    comment
):
    client = request.getfixturevalue(client_fixture)
    url = reverse(url_name, args=(comment.id,))
    response = client.get(url)

    if expected_status == HTTPStatus.FOUND:
        login_url = reverse(redirect_url)
        assertRedirects(response, f'{login_url}?next={url}')
    else:
        assert response.status_code == expected_status
