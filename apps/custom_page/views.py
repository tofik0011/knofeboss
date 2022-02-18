from django.http import Http404
from django.shortcuts import render, redirect
from .models import CustomPage


def view__custom_page(request, slug):
    slug = [str(x) for x in slug.split('/')]
    try:
        custom_p = CustomPage.get_custompage_by_url(slug[-1])
        if custom_p.redirect or custom_p.get_absolute_url() != request.path:
            return redirect(custom_p.get_absolute_url())
        return render(request, 'custom_page/custom_page.html', {'custom_page': custom_p})
    except Exception as ex:
        raise Http404("custom_page(request, slug): " + str(ex))
