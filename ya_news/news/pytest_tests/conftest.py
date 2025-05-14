import pytest
from django.test.client import Client
from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from news.models import News, Comment
from django.contrib.auth import get_user_model

User = get_user_model()


# Фикстуры для клиентов
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


# Фикстуры для новостей
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
    all_news = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(all_news)
    return all_news


# Фикстуры для комментариев
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
    return comments


# Фикстуры для URL
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


# Фикстуры для данных форм
@pytest.fixture
def comment_form_data():
    """Фикстура для данных формы комментария."""
    return {'text': 'Новый комментарий'}


@pytest.fixture
def bad_comment_form_data():
    """Фикстура для данных формы с запрещенными словами."""
    from news.forms import BAD_WORDS
    return {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
