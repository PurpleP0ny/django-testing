from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News

User = get_user_model()


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """Фикстура для постоянного доступа к БД"""
    pass


@pytest.fixture
def anonymous_client():
    """Фикстура для неавторизованного клиента."""
    return Client()


@pytest.fixture
def author():
    """Фикстура для создания пользователя-автора."""
    return User.objects.create(username='Автор')


@pytest.fixture
def author_client(author):
    """Фикстура для авторизованного клиента (автор)."""
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def reader():
    """Фикстура для создания пользователя-читателя."""
    return User.objects.create(username='Читатель')


@pytest.fixture
def reader_client(reader):
    """Фикстура для авторизованного клиента (читатель)."""
    client = Client()
    client.force_login(reader)
    return client


@pytest.fixture
def news():
    """Фикстура для создания новости."""
    return News.objects.create(
        title='Тестовая новость',
        text='Текст новости',
        date=datetime.today()
    )


@pytest.fixture
def bulk_news():
    """Фикстура для создания нескольких новостей."""
    today = datetime.today()
    News.objects.bulk_create(
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def comment(author, news):
    """Фикстура для создания комментария."""
    return Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )


@pytest.fixture
def bulk_comments(author, news):
    """Фикстура для создания нескольких комментариев."""
    now = timezone.now()
    comments = []
    for index in range(10):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=f'Текст {index}'
        )
        comment.created = now + timedelta(days=index)
        comment.save()
        comments.append(comment)


@pytest.fixture
def home_url():
    """Фикстура для URL главной страницы."""
    return reverse('news:home')


@pytest.fixture
def detail_url(news):
    """Фикстура для URL страницы новости."""
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def edit_url(comment):
    """Фикстура для URL редактирования комментария."""
    return reverse('news:edit', args=(comment.id,))


@pytest.fixture
def delete_url(comment):
    """Фикстура для URL удаления комментария."""
    return reverse('news:delete', args=(comment.id,))


@pytest.fixture
def login_url():
    """Фикстура для URL страницы входа."""
    return reverse('users:login')


@pytest.fixture
def signup_url():
    """Фикстура для URL страницы регистрации."""
    return reverse('users:signup')


@pytest.fixture
def logout_url():
    """Фикстура для URL страницы выхода."""
    return reverse('users:logout')
