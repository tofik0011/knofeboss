from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from apps.products_comparison.models import Comparison


def view__products_comparison(request):
    return render(request, 'products_comparison/comparison_page.html')


@csrf_exempt
def add_to_comparison(request):
    try:
        comparison = get_comparison(request)
        res = comparison.add_product(request.POST.get('product_id'))
        return JsonResponse(res)
    except Exception as e:
        print(str(e))
        return JsonResponse({'success': False})


@csrf_exempt
def del_from_comparison(request):
    try:
        comparison = get_comparison(request)
        res = comparison.del_product(request.POST.get('product_id'))
        return JsonResponse(res)
    except Exception as e:
        print(str(e))
        return JsonResponse({'success': False})


def get_comparison(request):
    try:
        comparison_id = request.session['comparison_id']
    except Exception as e:
        comparison = Comparison()
        comparison.save()
        comparison_id = comparison.id
        request.session['comparison_id'] = comparison_id
    return Comparison.objects.get(id=comparison_id)
