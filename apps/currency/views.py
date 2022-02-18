from decimal import Decimal, ROUND_CEILING
from django.http import HttpResponse
from apps.currency.models import Currency
from unine_engine import globals
from unine_engine.globals import DEFAULT_CURRENCY


def currency_set(request):
    code = request.POST.get('code', globals.CURRENCY_CODE_DEFAULT)
    return HttpResponse(currency_set_and_get(request, code))


def currency_get(request):
    return request.session['currency_code']


def get_currency_data_for_order(request):
    currency_code = currency_get(request)
    currency_obj = Currency.objects.get(code=currency_code)
    return {
        'code': currency_code,
        'value': str(currency_obj.value),
        'symbol_left': currency_obj.symbol_left,
        'symbol_right': currency_obj.symbol_right
    }


def currency_set_and_get(request, code=None):
    """
    Задає валюту магазину.
    Якщо в сесії немає валюти то записує
    Якщо в code приходить якась валюта то вона записується в сесію і вертається
    Якщо code = None то просто вертаємо валюту яка зараз в сесії
    """
    if 'currency_code' not in request.session:
        current_currency = Currency.objects.values_list('code', flat=True).filter(is_default=True).first()
        if current_currency is None or not current_currency:
            # Currency.objects.create(name='Grivna', code='UAH', symbol_left='', symbol_right='', value=Decimal(1), status=True, is_default=True)
            currency_main = Currency.objects.create(
                name=DEFAULT_CURRENCY['name'],
                code=DEFAULT_CURRENCY['code'],
                symbol_right=DEFAULT_CURRENCY['symbol_right'],
                value=DEFAULT_CURRENCY['value']
            )

            current_currency = Currency.objects.values_list('code', flat=True).filter(is_default=True).first()
        request.session['currency_code'] = current_currency
    if code:
        request.session['currency_code'] = code
    return request.session['currency_code']


def get_all_currencies():
    return Currency.objects.filter(status=True)


# TODO дві супер похожі функції шото подозрітельно
def convert_price(request, price, with_code=True):
    # try:
    currency_main = Currency.objects.get(is_default=True)
    currency = Currency.objects.get(code=currency_get(request))
    # except Exception as ex:
    #     # default = DEFAULT_CURRENCY
    #     # currency = currency_main = Currency.objects.create(
    #     #     name=default['name'],
    #     #     code=default['code'],
    #     #     symbol_right=default['symbol_right'],
    #     #     value=default['value'])
    #     print(ex)
    # print('121',type(price),type(currency_main.value),type(currency.value))
    if price:
        price = price * Decimal(currency_main.value) * Decimal(currency.value)
    else:
        price = 0
    res = Decimal(price).quantize(Decimal('.00'), rounding=ROUND_CEILING)
    if with_code:
        return f'{currency.symbol_left}{res}{currency.symbol_right}'
    else:
        return f'{res}'


def convert_price_by_currency_code(code, price):
    try:
        currency_main = Currency.objects.get(is_default=True)
        currency = Currency.objects.get(code=code)
        if price:
            price = price * currency_main.value * currency.value
    except Exception as ex:
        price = 0
        print(ex)
    return Decimal(price).quantize(Decimal('.00'), rounding=ROUND_CEILING)
