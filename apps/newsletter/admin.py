from django.contrib import admin
from .models import NewsletterUser, NewsletterMailing

@admin.register(NewsletterUser)
class NewsletterUserAdmin(admin.ModelAdmin):
    list_display = ("id", "mail", "added_date")

    class Meta:
        model = NewsletterUser


@admin.register(NewsletterMailing)
class NewsletterMailingAdmin(admin.ModelAdmin):
    list_display = ("id", "subject", "content", "added_date")

    class Meta:
        model = NewsletterMailing
