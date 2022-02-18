from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, redirect
from unine_engine.globals import BLOG_ITEMS_PER_PAGE
from .models import Article, Category


def view__blog(request):
    articles = Article.objects.filter(active=True).order_by('-added_date')
    paginator = Paginator(articles, BLOG_ITEMS_PER_PAGE)
    if request.method == "GET":
        page = paginator.page(request.GET.get('page', 1))
        articles = page
    result_request = {
        "categories": Category.get_all_categories(),
        "articles": articles,
    }
    return render(request, 'blog/blog.html', result_request)


def view__article_or_category(request, category_link):
    category_slugs = [str(x) for x in category_link.split('/')]
    try:
        article = Article.get_article_by_url(category_slugs[-1])
        """ Якщо ссилка в іншій мові відрізняється то перейти на неї """
        if article.get_absolute_url() != request.path:
            return redirect(article.get_absolute_url())
        result_request = {
            "article": article,
            "category": article.category_fk,
            "categories": Category.get_all_categories(),
        }
        return render(request, 'blog/article.html', result_request)
    except Exception as ex:
        print("not article", ex)

    try:
        category = Category.get_category_by_url(category_slugs[-1])

        """ Якщо ссилка в іншій мові відрізняється то перейти на неї """
        if category.get_absolute_url() != request.path:
            return redirect(category.get_absolute_url())

        articles = Category.get_all_articles_in_category(category.pk)
        paginator = Paginator(articles, BLOG_ITEMS_PER_PAGE)
        if request.method == "GET":
            page = paginator.page(request.GET.get('page', 1))
            articles = page
        result_request = {
            "category": category,
            "categories": Category.get_all_categories(),
            "categories_children": category.get_all_children(),
            "articles": articles,
        }
        return render(request, 'blog/category.html', result_request)
    except Exception as ex:
        print("not category", ex)

    raise Http404("NotProductAndNOtCategory")
