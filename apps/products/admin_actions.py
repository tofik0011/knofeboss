from slugify import slugify
from unine_engine.settings import LANGUAGES
from .models import Category, Product


def action_copy_category(modeladmin, request, queryset):
    for category in queryset:
        _temp_category = category
        _temp_category.pk = None
        _temp_category.active = False
        _temp_category.save()
        for lang in LANGUAGES:
            _temp_category.__setattr__(f'link_{lang[0]}', f"{slugify(_temp_category.__getattribute__(f'link_{lang[0]}'), to_lower=True)}_new_{_temp_category.id}")
        _temp_category.save()


def action_copy_product(modeladmin, request, queryset):
    for product in queryset:
        _temp_product = Product.objects.get(id=product.id)
        _temp_product.pk = None
        _temp_product.active = True
        _temp_product.save()
        _temp_product.show_in_categories.set(product.show_in_categories.all())
        for o_o_p in product.optionofproduct_set.all():
            _temp_product.optionofproduct_set.create(
                option_fk_id=o_o_p.option_fk_id,
                option_value_fk_id=o_o_p.option_value_fk_id,
                qty=o_o_p.qty,
                price=o_o_p.price,
            )
        for a_o_p in product.attributeofproduct_set.all():
            _temp_product.attributeofproduct_set.create(
                attribute_fk_id=a_o_p.attribute_fk_id,
                attribute_value_fk_id=a_o_p.attribute_value_fk_id,
            )
        for f_o_p in product.filterofproduct_set.all():
            _temp_product.filterofproduct_set.create(
                filter_fk_id=f_o_p.filter_fk_id,
                filter_value_fk_id=f_o_p.filter_value_fk_id,
            )
        for lang in LANGUAGES:
            _temp_product.__setattr__(f'link_{lang[0]}', f"{slugify(_temp_product.__getattribute__(f'link_{lang[0]}'), to_lower=True)}_new_{_temp_product.id}")
        _temp_product.save()
