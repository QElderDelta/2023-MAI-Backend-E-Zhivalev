from django.urls import path
from . import views

urlpatterns = [
    path('api/listings/', views.all_listings, name='all_listings'),
    path('api/listings/<int:id>/',
         views.ListingView.as_view(http_method_names=['get']), name='listing_by_id'),
    path('api/listings/create/',
         views.ListingView.as_view(http_method_names=['post']), name='add_listing'),
    path('api/listings/search',
         views.search_by_query, name='search_by_query'),
    path('api/user/<int:id>',
         views.get_user_profile, name='get_user_profile'),
    path('api/user/create/',
         views.add_user, name='add_user')
]
