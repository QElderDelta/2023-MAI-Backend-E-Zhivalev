from rest_framework import serializers
from .models import Listing


class ListingSerializer(serializers.ModelSerializer):
    car_brand = serializers.SlugRelatedField(slug_field='name', read_only=True)
    car_model = serializers.SlugRelatedField(slug_field='name', read_only=True)
    engine_type = serializers.SlugRelatedField(
        slug_field='name', read_only=True)

    class Meta:
        model = Listing

        read_only_fields = ['car_brand', 'car_model', 'mileage',
                            'number_of_owners', 'engine_type', 'engine_volume', 'horse_power']

        fields = read_only_fields + ['price']
