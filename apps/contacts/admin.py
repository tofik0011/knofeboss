from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from apps.contacts.models import Email, SocialNetwork, Phone, Address


@admin.register(Address)
class AddressAdmin(TabbedTranslationAdmin):
    list_display = [field.name for field in Address._meta.fields]
    list_editable = [field.name for field in Address._meta.fields if field.name != "id"]

    class Meta:
        model = Address


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Email._meta.fields]
    list_editable = [field.name for field in Email._meta.fields if field.name != "id" and field.name != "added_date" and field.name != "update_date"]
    search_fields = ('name',)

    class Meta:
        model = Email


@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Phone._meta.fields]
    list_editable = [field.name for field in Phone._meta.fields if field.name != "id"]
    search_fields = ('name',)

    class Meta:
        model = Phone


@admin.register(SocialNetwork)
class SocialNetworkAdmin(admin.ModelAdmin):
    list_display = [field.name for field in SocialNetwork._meta.fields]
    list_editable = [field.name for field in SocialNetwork._meta.fields if field.name != "id"]

    class Meta:
        model = SocialNetwork
