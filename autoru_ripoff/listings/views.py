from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseBadRequest
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from rest_framework import generics

from .models import *
from .serializers import ListingSerializer


class ListingView(View):
    manual_fields = ['car_brand', 'car_model', 'engine_type']

    def convert_field_with_indices(obj: dict):
        for field_name, model in zip(ListingView.manual_fields, [CarBrand, CarModel, EngineType]):
            actual_value = get_object_or_404(model, pk=obj[field_name]).name

            obj[field_name] = actual_value

        return obj

    def get(self, request, id=None):
        if id is None or id < 0:
            return HttpResponseBadRequest()

        return JsonResponse({'listing': ListingView.convert_field_with_indices(
            model_to_dict(get_object_or_404(Listing, pk=id)))})

    def post(self, request):
        listing = Listing()

        for field in listing._meta.get_fields():
            field_name = field.name

            if field_name in ListingView.manual_fields or field_name == 'id':
                continue

            field_value = request.POST.get(field_name)

            if field_value is None:
                return HttpResponseBadRequest(f'Missing field {field_name}')

            setattr(listing, field_name, field_value)

        for field_name, model in zip(ListingView.manual_fields, [CarBrand, CarModel, EngineType]):
            field_value = request.POST.get(field_name)

            if field_value is None:
                return HttpResponseBadRequest(f'Missing field {field_name}')

            actual_object = model.objects.filter(
                name=field_value)

            if len(actual_object) != 1:
                return HttpResponseBadRequest(f'Field {field_name} has invalid value')

            setattr(listing, field_name, model(pk=actual_object[0].id))

        listing.save()

        return JsonResponse({'listing': {'id': f'{listing.id}'}})


class ListingsList(generics.ListAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer


class SingleListing(generics.RetrieveUpdateDestroyAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer


@require_http_methods(['GET'])
def search_by_query(request):
    query = request.GET.get('q')

    if query is None:
        return HttpResponseBadRequest(f'Missing query parameter')

    result = []

    car_brands = list(
        map(lambda x: x.id, CarBrand.objects.filter(name__icontains=query)))
    car_models = list(
        map(lambda x: x.id, CarModel.objects.filter(name__icontains=query)))

    for entry in Listing.objects.filter(Q(car_brand__in=car_brands) | Q(car_model__in=car_models)):
        result.append(ListingView.convert_field_with_indices(
            model_to_dict(entry)))

    return JsonResponse({'listings': result})
