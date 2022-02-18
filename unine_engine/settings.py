import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'v#3)(#s03gfc^_s&gk42fom&9t5-7h_n#gn%m1g4wv+-8x+ncb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'custom_admin',
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'import_export',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'mainapp',
    'apps.currency.apps.CurrencyConfig',
    'apps.logger',
    'apps.newsletter.apps.NewsletterConfig',
    'apps.blog.apps.BlogConfig',
    'apps.products.apps.ProductsConfig',
    'apps.contacts.apps.ContactsConfig',
    'apps.checkout.apps.CheckoutConfig',
    'apps.testimonials.apps.TesttimonialsConfig',
    'apps.feedback_form.apps.FeedbackFormConfig',
    'apps.nova_poshta',
    'apps.email_notifications.apps.EmailNotificationsConfig',
    'apps.banner.apps.BannerConfig',
    'apps.custom_page.apps.CustomPageConfig',
    'apps.products_comparison.apps.ProductsComparsionConfig',
    'apps.profile.apps.AccountConfig',
    'apps.menu.apps.MenuConfig',
    'sorl.thumbnail',
    'mptt',
    'tabbed_admin',
    'ckeditor',
    'ckeditor_uploader',
    'filebrowser',
    'slugify',
    # 'easy_select2',
    'social_django',
    'rest_framework',
    'rest_framework.authtoken',
    'smart_selects',
    'django_user_agents',
    # 'oauth2_provider',
    'apps.redirects',
]
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (

        # 'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',  # To keep the Browsable API
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_currentuser.middleware.ThreadLocalUserMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
    # 'oauth2_provider.middleware.OAuth2TokenMiddleware',
    'apps.redirects.middleware.RedirectsMiddleware',
]

ROOT_URLCONF = 'unine_engine.urls'

CKEDITOR_UPLOAD_PATH = "uploads/"

CKEDITOR_IMAGE_BACKEND = "pillow"

CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
        # 'skin': 'office2013',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_YourCustomToolbarConfig': [
            {'name': 'document', 'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates']},
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
            {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
            {'name': 'forms',
             'items': ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
                       'HiddenField']},
            '/',
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
                       'Language']},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            {'name': 'insert',
             'items': ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']},
            '/',
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
            {'name': 'about', 'items': ['About']},
            '/',  # put this to force next toolbar on new line
            {'name': 'yourcustomtools', 'items': [
                # put the name of your editor.ui.addButton here
                'Preview',
                'Maximize',

            ]},
        ],
        'toolbar': 'YourCustomToolbarConfig',  # put selected toolbar config here
        # 'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
        # 'height': 291,
        # 'width': '100%',
        # 'filebrowserWindowHeight': 725,
        # 'filebrowserWindowWidth': 940,
        # 'toolbarCanCollapse': True,
        # 'mathJaxLib': '//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML',
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            'uploadimage',  # the upload image feature
            # your extra plugins here
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            # 'devtools',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath'
        ]),
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'unine_engine.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'OPTIONS': {
            'timeout': 20,
        }
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'unine_engine_2020',
#         'USER': 'unine_engine',
#         'PASSWORD': 'unine_engine',
#         'HOST': 'localhost',
#         'OPTIONS': {
#             'init_command': "SET storage_engine=INNODB; SET sql_mode='STRICT_TRANS_TABLES'; SET innodb_strict_mode=1; innodb_large_prefix = TRUE;innodb_file_format = Barracuda;innodb_file_per_table = TRUE;",
#             'charset': 'utf8',
#
#         },
#     }
# }
# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

FILEBROWSER_VERSIONS = {
    'product_thumbnail': {'verbose_name': 'Product Thumbnail', 'width': 290, 'height': 350, 'opts': 'crop'},
    'product_min': {'verbose_name': 'Product Thumbnail', 'width': 350, 'height': 350, 'opts': 'crop'},
    'admin_thumbnail': {'verbose_name': 'Admin Thumbnail', 'width': 60, 'height': 60, 'opts': 'crop'},
    'thumbnail': {'verbose_name': 'Thumbnail (1 col)', 'width': 60, 'height': 60, 'opts': 'crop'},
    'full_hd': {'verbose_name': 'Full HD', 'width': 1920, 'height': 1080, 'opts': 'crop'},
    '40x40': {'verbose_name': '40x40', 'width': 40, 'height': 40, 'opts': 'crop'},
    '80x80': {'verbose_name': '80x80', 'width': 80, 'height': 80, 'opts': 'crop'},
    '100x100': {'verbose_name': '80x80', 'width': 100, 'height': 100, 'opts': 'crop'},
}

FILEBROWSER_ADMIN_VERSIONS = ['product_thumbnail', 'thumbnail', 'admin_thumbnail']
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'uk'

LANGUAGES = (
    ('uk', u'Українська'),
    ('ru', u'Русский'),
)

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

DATA_UPLOAD_MAX_NUMBER_FIELDS = 100000

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
FILEBROWSER_DIRECTORY = ''
DIRECTORY = ''
FILE_UPLOAD_PERMISSIONS = 0o666

TABBED_ADMIN_USE_JQUERY_UI = True
TABBED_ADMIN_JQUERY_UI_CSS = '/static/jquery/jquery-ui.css'
TABBED_ADMIN_JQUERY_UI_JS = '/static/jquery/jquery-ui.js'

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locate')
]

DEFAULT_JQUERY_UI_JS = '/static/jquery/jquery-ui.js'
SELECT2_USE_BUNDLED_JQUERY = False

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.instagram.InstagramOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    # 'oauth2_provider.backends.OAuth2Backend',
)
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',
    # 'auth_pipeline.create_user',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

#
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '21508780786-mb94vmvfebr970poheesqem2sq36iqvc.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '0WHmIrenUPXcjbLE9t5srUqO'
LOGIN_URL = 'view__login'
LOGIN_REDIRECT_URL = '/order_history/'
# LOGIN_REDIRECT_URL = '/complete_auth/'
LOGOUT_REDIRECT_URL = '/'
SOCIAL_AUTH_URL_NAMESPACE = 'social'  # якшо треба кастом namespace
# LOGIN_URL = 'view__login'
LOGOUT_URL = 'index'
# LOGIN_REDIRECT_URL = 'index'

SOCIAL_AUTH_FACEBOOK_KEY = "2757565854508740"  # App ID
SOCIAL_AUTH_FACEBOOK_SECRET = "0028ab9879231d594312e563e4e852bf"  # App ID
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', ]  # add this
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'locale': 'ru_RU',
    'fields': 'id, name, email, picture.type(large)'
}
SOCIAL_AUTH_FACEBOOK_EXTRA_DATA = [  # add this
    ('name', 'name'),
    ('email', 'email'),
    ('picture', 'picture'),
]

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST_USER = 'u9smtp@gmail.com'
EMAIL_HOST_PASSWORD = 'Qweqwe123123'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = 'u9smtp@gmail.com'
DEFAULT_FROM_TO = 'u9smtp@gmail.com'
EMAIL_USE_TLS = True

SOCIAL_AUTH_INSTAGRAM_KEY = os.environ.get('INSTAGRAM_KEY')  # App ID
SOCIAL_AUTH_INSTAGRAM_SECRET = os.environ.get('INSTAGRAM_SECRET')  # App Secret

FILEBROWSER_EXTENSIONS = {
    'Image': ['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff'],
    'Document': ['.pdf', '.doc', '.rtf', '.txt', '.xls', '.csv', '.xml'],
    'Video': ['.mov', '.wmv', '.mpeg', '.mpg', '.avi', '.rm'],
    'Audio': ['.mp3', '.mp4', '.wav', '.aiff', '.midi', '.m4p']
}

REDIS_HOST = '127.0.0.1'
REDIS_PORT = '6379'
CELERY_BROKER_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
AUTH_USER_MODEL = 'profile.Profile'

JQUERY_URL = False  # smart_selects
# USE_DJANGO_JQUERY = True # smart_selects


LIQPAY_SANDBOX = 1
LIQPAY_PUBLIC_KEY = 'sandbox_i2314689470'
LIQPAY_PRIVATE_KEY = 'sandbox_Nbzs1JkYW2Ci1WCVycBjLWHneQkwfkff7qjaaVsx'