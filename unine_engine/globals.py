from django.utils.translation import gettext_lazy as _
from unine_engine.settings import *

CURRENCY_CODE_DEFAULT = 'UAH'
SITE_NAME = 'Site name'
SITE_HOST = 'http://127.0.0.1:8000/'
# NOVA POSHTA
NP_API_KEY = '747bbbde16addd0b8c5989205d0a325f'
NP_API_URL = 'https://api.novaposhta.ua/v2.0/json/'
PRICE_ONLY_FOR_REGISTERED = True
VISITED_PRODUCTS_LIMIT = 8
PRODUCTS_SORTING = (
    # ('id', _('price_default')),  # За замовчуванням
    ('calc_price', _('price_cheap_to_expensive')),  # Від дешевих до дорогих
    ('-calc_price', _('price_expensive_to_cheap')),  # Від дорогих до дешевих
    # ('-added_date', _('price_new_to_old')),  # Від нових до старих
)

PRODUCTS_SEARCH_BY_QUERY_LIMIT = 5
PRODUCTS_PER_PAGE = 30
REVIEWS_PER_PAGE = 2
BLOG_ITEMS_PER_PAGE = 6

ORDER_STATUS_CHOICES = (
    ('new', _('order_status__new')),
    ('canceled', _('order_status__canceled')),
    ('pending', _('order_status__pending')),
    ('sent', _('order_status__sent')),
    ('completed', _('order_status__completed'))
)

MENU_CHOICES = (
    ('main', _("menu__main_menu")),
    ('top', _("menu__top_menu")),
    ('bottom', _("menu__bottom_menu")),
)

DELIVERY_CHOICES = (
    ('pickup', _('pickup')),
    ('new_post', _('new_post')),
    ('avtoluks', _('avtoluks')),
    ('in_time', _('in_time')),
    ('delivery', _('delivery')),
    ('ukr_post', _('ukr_post')),
)

DISCOUNT_CHOICES = (
    ('percentage', _("products__discount_with_percantage")),
    ('sum', _("products__discount_with_sum")),
)

PAYMENT_CHOICES = (
    ('cod', _('cod')),
    ('liqpay', _('liqpay'))
)

OPTION_OPERATION = (
    ('add', '+'),
    ('equal', '='),
)

USER_TYPES = (
    ('default', _('account__default')),
    ('wholesale', _('account__wholesale')),
    ('retail', _('account__retail')),
)

# EMAIL_HOST      = 'my-domain.com'
# EMAIL_HOST_PASSWORD = 'my cpanel password'
# EMAIL_HOST_USER = 'my cpanel user'
# EMAIL_PORT      = 25
# EMAIL_USE_TLS   = False
# DEFAULT_FROM_EMAIL  = 'webmaster@my-host.com'
# SERVER_EMAIL    = 'root@my-domain.com'

EMAIL_KEYWORDS = (
    ('footer', 'Показывать в футере'),
    ('contacts', 'Отображать на странице контактов'),
    ('checkout', 'Оповещения о новых заказах'),
    ('feedback_form', 'Зворотній звязок'),
)

ADDRESS_KEYWORDS = (
    ('footer', 'Показывать в футере'),
    ('contacts', 'Отображать на странице контактов'),
)
PHONE_KEYWORDS = (
    ('footer', 'Показывать в футере'),
    ('contacts', 'Отображать на странице контактов'),
)

TEXT_CONTENT_KEYWORDS = (
    ('ua_production', "Главная - Украинское производство"),
    ('mission_1', "Главная - Миссия"),
    ('mission_2', "Главная - Видение"),
    ('retail_districts', "Розничным - Список областей"),
    ('mainpage_h1', "Главная - H1"),
)

SEO_DATA_KEYWORDS = (
    ('mainpage', "Главная Страница"),
    ('blog', "Блог"),
    ('catalog', "Каталог"),
    ('contacts', "Контакты"),
    ('reviews', "Отзывы"),
)
DEFAULT_CURRENCY = {'name': 'Hryvna', 'code': 'UAH', 'symbol_right': 'грн', 'value': 1.0}
ADMIN_ORDERING = {
    'products': 3,
    'checkout': 1,
    'mainapp': 4,
    'auth': 2,
    'menu': 5,
}

# Creating a sort function
def get_app_list(self, request):
    app_dict = self._build_app_dict(request)

    def sort_apps(element):
        if element['app_label'].lower() in ADMIN_ORDERING:
            return ADMIN_ORDERING[element['app_label'].lower()]
        else:
            return 999

    app_list = sorted(app_dict.values(), key=sort_apps)
    for app in app_list:
        app['models'].sort(key=lambda x: x['name'])
    return app_list
    #     app = app_dict[app_name]
    #     app['models'].sort(key=lambda x: object_list.index(x['object_name']))
    #     yield app

# Covering django.contrib.admin.AdminSite.get_app_list
from django.contrib import admin

admin.AdminSite.get_app_list = get_app_list
# end region ADMIN ORDERING