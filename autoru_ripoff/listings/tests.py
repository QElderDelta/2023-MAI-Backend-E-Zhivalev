from django.test import TestCase
import factory
import random
from rest_framework.test import APIClient
from unittest.mock import patch

from .models import *


class ListingsTest(TestCase):
    def setUp(self):
        bmw = CarBrand.objects.create(name='BMW')
        audi = CarBrand.objects.create(name='Audi')
        porsche = CarBrand.objects.create(name='Porsche')

        car_models = []
        car_models.append(CarModel.objects.create(brand_id=bmw, name='X3'))
        car_models.append(CarModel.objects.create(brand_id=bmw, name='X5'))
        car_models.append(CarModel.objects.create(brand_id=audi, name='RS6'))
        car_models.append(CarModel.objects.create(brand_id=audi, name='Q7'))
        car_models.append(CarModel.objects.create(
            brand_id=porsche, name='911'))
        car_models.append(CarModel.objects.create(
            brand_id=porsche, name='Cayenne'))

        engine_types = []
        engine_types.append(EngineType.objects.create(name='Petrol'))
        engine_types.append(EngineType.objects.create(name='Diesel'))

        class ListingFactory(factory.django.DjangoModelFactory):
            class Meta:
                model = Listing

            car_model = car_models[random.randint(0, len(car_models) - 1)]
            car_brand = car_model.brand_id
            engine_type = engine_types[random.randint(
                0, len(engine_types) - 1)]

            price = random.randint(1000000, 5000000)
            mileage = random.randint(0, 300000)
            number_of_owners = random.randint(0, 5)
            engine_volume = random.randint(1, 5)
            horse_power = random.randint(100, 717)

        self.listing_factory = ListingFactory

        self.client = APIClient()

    def test_add_listing(self):
        listing_data = {
            'car_brand': 'BMW',
            'car_model': 'X5',
            'price': 2300000,
            'mileage': 4000,
            'number_of_owners': 2,
            'engine_type': 'Diesel',
            'engine_volume': 3.0,
            'horse_power': 249
        }

        res = self.client.post(
            '/api/listings/create/', data=listing_data)
        self.assertEqual(res.status_code, 200, res.content)

        listing_id = res.json()['listing']['id']

        res = self.client.get(f'/api/listings/{listing_id}/')
        self.assertEqual(res.status_code, 200, res.content)
        self.assertEqual(res.json(), listing_data)

        listing_data['car_brand'] = 'Land Rover'
        res = self.client.post(
            '/api/listings/create/', data=listing_data)
        self.assertEqual(res.status_code, 400)

    def test_listing_update_delete(self):
        listing_data = {
            'car_brand': 'BMW',
            'car_model': 'X5',
            'price': 2300000,
            'mileage': 4000,
            'number_of_owners': 2,
            'engine_type': 'Diesel',
            'engine_volume': 3.0,
            'horse_power': 249
        }

        res = self.client.post(
            '/api/listings/create/', data=listing_data)
        self.assertEqual(res.status_code, 200, res.content)

        listing_id = res.json()['listing']['id']

        res = self.client.get(f'/api/listings/{listing_id}/')
        self.assertEqual(res.status_code, 200, res.content)
        self.assertEqual(res.json()['price'], 2300000)

        res = self.client.put(
            f'/api/listings/{listing_id}/', data={'price': 2500000})
        self.assertEqual(res.status_code, 200, res.content)

        res = self.client.get(f'/api/listings/{listing_id}/')
        self.assertEqual(res.status_code, 200, res.content)
        self.assertEqual(res.json()['price'], 2500000)

        res = self.client.delete(f'/api/listings/{listing_id}/')
        self.assertEqual(res.status_code, 204, res.content)

        res = self.client.get(f'/api/listings/{listing_id}/')
        self.assertEqual(res.status_code, 404, res.content)

    def test_get_all_listings(self):
        LISTING_COUNT = 3
        listings = []

        for _ in range(LISTING_COUNT):
            listings.append(self.listing_factory.create())

        res = self.client.get(f'/api/listings/')
        self.assertEqual(res.status_code, 200, res.content)
        self.assertEqual(len(res.json()), LISTING_COUNT)

    def test_search_listings(self):
        listing_data = {
            'car_brand': 'BMW',
            'car_model': 'X5',
            'price': 2300000,
            'mileage': 4000,
            'number_of_owners': 2,
            'engine_type': 'Diesel',
            'engine_volume': 3.0,
            'horse_power': 249
        }

        res = self.client.post(
            '/api/listings/create/', data=listing_data)
        self.assertEqual(res.status_code, 200, res.content)

        listing_data['car_model'] = 'X3'
        res = self.client.post(
            '/api/listings/create/', data=listing_data)
        self.assertEqual(res.status_code, 200, res.content)

        res = self.client.get(
            '/api/listings/search?q=BMW')
        self.assertEqual(res.status_code, 200, res.content)
        self.assertEqual(len(res.json()['listings']), 2)

        res = self.client.get(
            '/api/listings/search?q=X5')
        self.assertEqual(res.status_code, 200, res.content)
        self.assertEqual(len(res.json()['listings']), 1)
        self.assertEqual(res.json()['listings'][0]['car_model'], 'X5')

        res = self.client.get(
            '/api/listings/search?q=X3')
        self.assertEqual(res.status_code, 200, res.content)
        self.assertEqual(len(res.json()['listings']), 1)
        self.assertEqual(res.json()['listings'][0]['car_model'], 'X3')

        res = self.client.get(
            '/api/listings/search?q=Audi')
        self.assertEqual(res.status_code, 200, res.content)
        self.assertEqual(len(res.json()['listings']), 0)

    @patch('listings.models.Listing.objects.filter')
    def test_search_calls_filter(self, filter_mock):
        res = self.client.get(
            '/api/listings/search?q=BMW')
        self.assertEqual(res.status_code, 200, res.content)

        self.assertEqual(int(filter_mock.called_count), 1)
