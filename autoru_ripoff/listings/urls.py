from django.urls import path
from . import views

urlpatterns = [
    path('api/listings/', views.ListingsList.as_view(), name='all_listings'),
    path('api/listings/<int:pk>/',
         views.SingleListing.as_view(), name='listing_by_id'),
    path('api/listings/create/',
         views.ListingView.as_view(http_method_names=['post']), name='add_listing'),
    path('api/listings/search',
         views.search_by_query, name='search_by_query')
]
