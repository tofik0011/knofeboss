# from django.contrib import admin
# from .models import Region, Settlement
#
#
# @admin.register(Region)
# class AdminRegion(admin.ModelAdmin):
#     list_display = [field.name for field in Region._meta.fields]
#     list_editable = [field.name for field in Region._meta.fields if field.name != "id"]
#
#     class Meta:
#         model = Region
#
#
# @admin.register(Settlement)
# class AdminSettlement(admin.ModelAdmin):
#     list_display = [field.name for field in Settlement._meta.fields]
#     list_editable = [field.name for field in Settlement._meta.fields if field.name != "id"]
#     search_fields = ['name', 'id_in_file']
#
#     class Meta:
#         model = Settlement

