from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'url, client, expected_status',
    [
        (lazy_fixture('home_url'),
         lazy_fixture('anonymous_client'),
         HTTPStatus.OK),
        (lazy_fixture('detail_url'),
         lazy_fixture('anonymous_client'),
         HTTPStatus.OK),
        (lazy_fixture('login_url'),
         lazy_fixture('anonymous_client'),
         HTTPStatus.OK),
        (lazy_fixture('signup_url'),
         lazy_fixture('anonymous_client'),
         HTTPStatus.OK),
    ],
    ids=['home', 'detail', 'login', 'signup']
)
def test_pages_availability(url, client, expected_status):
    response = client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url, client, expected_status, redirect_url',
    [
        (lazy_fixture('edit_url'),
         lazy_fixture('anonymous_client'),
         HTTPStatus.FOUND,
         lazy_fixture('login_url')),
        (lazy_fixture('delete_url'),
         lazy_fixture('anonymous_client'),
         HTTPStatus.FOUND,
         lazy_fixture('login_url')),
        (lazy_fixture('edit_url'),
         lazy_fixture('reader_client'),
         HTTPStatus.NOT_FOUND,
         None),
        (lazy_fixture('delete_url'),
         lazy_fixture('reader_client'),
         HTTPStatus.NOT_FOUND,
         None),
        (lazy_fixture('edit_url'),
         lazy_fixture('author_client'),
         HTTPStatus.OK,
         None),
        (lazy_fixture('delete_url'),
         lazy_fixture('author_client'),
         HTTPStatus.OK,
         None),
    ],
    ids=[
        'anon_edit',
        'anon_delete',
        'reader_edit',
        'reader_delete',
        'author_edit',
        'author_delete'
    ]
)
def test_comment_actions_availability(
    url,
    client,
    expected_status,
    redirect_url
):
    response = client.get(url)

    if expected_status == HTTPStatus.FOUND:
        assertRedirects(response, f'{redirect_url}?next={url}')
    else:
        assert response.status_code == expected_status
