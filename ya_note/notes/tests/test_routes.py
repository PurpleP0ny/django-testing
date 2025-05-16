from http import HTTPStatus

from django.contrib.auth import get_user_model

from .common import (ADD_URL, DELETE_URL, DETAIL_URL, EDIT_URL, HOME_URL,
                     LIST_URL, LOGIN_URL, LOGOUT_URL, SIGNUP_URL, SUCCESS_URL,
                     TestCaseWithData)

User = get_user_model()


class TestRoutes(TestCaseWithData):
    def test_status_codes(self):
        """Проверка статус-кодов для разных пользователей."""
        test_cases = [
            {
                'url': HOME_URL,
                'client': self.client,
                'expected_status': HTTPStatus.OK,
            },
            {
                'url': LOGIN_URL,
                'client': self.client,
                'expected_status': HTTPStatus.OK,
            },
            {
                'url': SIGNUP_URL,
                'client': self.client,
                'expected_status': HTTPStatus.OK,
            },
            {
                'url': LIST_URL,
                'client': self.auth_client,
                'expected_status': HTTPStatus.OK,
            },
            {
                'url': ADD_URL,
                'client': self.auth_client,
                'expected_status': HTTPStatus.OK,
            },
            {
                'url': SUCCESS_URL,
                'client': self.auth_client,
                'expected_status': HTTPStatus.OK,
            },
            {
                'url': DETAIL_URL,
                'client': self.author_client,
                'expected_status': HTTPStatus.OK,
            },
            {
                'url': EDIT_URL,
                'client': self.author_client,
                'expected_status': HTTPStatus.OK,
            },
            {
                'url': DELETE_URL,
                'client': self.author_client,
                'expected_status': HTTPStatus.OK,
            },
        ]

        for case in test_cases:
            with self.subTest(url=case['url'],
                              expected_status=case['expected_status']):
                response = case['client'].get(case['url'])
                self.assertEqual(response.status_code, case['expected_status'])

    def test_redirects_for_anonymous(self):
        """Проверка редиректов для анонимных пользователей."""
        test_cases = [
            {
                'url': LIST_URL,
                'expected_redirect': f'{LOGIN_URL}?next={LIST_URL}',
            },
            {
                'url': ADD_URL,
                'expected_redirect': f'{LOGIN_URL}?next={ADD_URL}',
            },
            {
                'url': SUCCESS_URL,
                'expected_redirect': f'{LOGIN_URL}?next={SUCCESS_URL}',
            },
            {
                'url': DETAIL_URL,
                'expected_redirect': f'{LOGIN_URL}?next={DETAIL_URL}',
            },
            {
                'url': EDIT_URL,
                'expected_redirect': f'{LOGIN_URL}?next={EDIT_URL}',
            },
            {
                'url': DELETE_URL,
                'expected_redirect': f'{LOGIN_URL}?next={DELETE_URL}',
            },
        ]

        for case in test_cases:
            with self.subTest(url=case['url'], user='anonymous'):
                response = self.client.get(case['url'])
                self.assertRedirects(response, case['expected_redirect'])

    def test_logout_behavior(self):
        """Проверка поведения при выходе из системы."""
        test_cases = [
            {
                'client': self.client,
                'username': 'anonymous',
                'expected_status': HTTPStatus.OK,
            },
            {
                'client': self.auth_client,
                'username': self.user.username,
                'expected_status': HTTPStatus.OK,
            },
            {
                'client': self.author_client,
                'username': self.author.username,
                'expected_status': HTTPStatus.OK,
            },
        ]

        for case in test_cases:
            with self.subTest(user=case['username']):
                response = case['client'].post(LOGOUT_URL)
                self.assertEqual(response.status_code, case['expected_status'])
