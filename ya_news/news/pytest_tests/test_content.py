import pytest
from django.conf import settings

pytestmark = pytest.mark.django_db


def test_news_home_page_context(anonymous_client, home_url, bulk_news):
    response = anonymous_client.get(home_url)
    assert 'object_list' in response.context


def test_news_count(anonymous_client, home_url, bulk_news):
    response = anonymous_client.get(home_url)
    object_list = response.context["object_list"]
    assert object_list.count() == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(anonymous_client, home_url, bulk_news):
    response = anonymous_client.get(home_url)
    object_list = response.context["object_list"]
    all_dates = [news.date for news in object_list]
    assert all_dates == sorted(all_dates, reverse=True)


def test_comments_order(anonymous_client, detail_url, bulk_comments):
    response = anonymous_client.get(detail_url)
    news = response.context["news"]
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    assert all_timestamps == sorted(all_timestamps)


def test_anonymous_client_has_no_form(anonymous_client, detail_url):
    response = anonymous_client.get(detail_url)
    assert "form" not in response.context


def test_authorized_client_has_form(author_client, detail_url):
    response = author_client.get(detail_url)
    assert "form" in response.context
    from news.forms import CommentForm
    assert isinstance(response.context["form"], CommentForm)
