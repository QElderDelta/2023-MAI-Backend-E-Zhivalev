from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseBadRequest
from django.views import View
from django.views.decorators.http import require_http_methods


class ListingView(View):
    def get(self, request, id=None):
        if id is None or id < 0:
            return HttpResponseBadRequest()

        return JsonResponse({})

    def post(self, request):
        return JsonResponse({'listing': {'id': ''}})


@require_http_methods(['GET'])
def all_listings(request):
    return JsonResponse({'listings': []})


@require_http_methods(['GET'])
def listings_for_brand(request, brand):
    return JsonResponse({'listings': []})


@require_http_methods(['GET'])
def search_by_query(request, query):
    return JsonResponse({'listings': []})


@require_http_methods(['GET'])
def get_user_profile(request, id):
    return JsonResponse({'id': f'{id}'})


@require_http_methods(['POST'])
def add_user(request):
    return JsonResponse({})
