from django.contrib import admin
from .models import Testimonial


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("pk", "author", "active")
    list_editable = ("active",)

    class Meta:
        model = Testimonial


admin.site.register(Testimonial, ReviewAdmin)
