from django.urls import path
from watchlist.views import (
    WatchListView, 
    MovieDetailView,
    StreamPlatformListView, 
    StreamPlatformDetailView, 
    ReviewListView,
    ReviewDetailView,
    ReviewCreateView,
    LogoutView,
)

urlpatterns = [
    path('', WatchListView.as_view(), name='watch-list'),    
    path('<int:pk>/', MovieDetailView.as_view(), name='movie-detail'),    
    path('stream/', StreamPlatformListView.as_view(), name='platform-list'),    
    path('stream/<int:pk>/', StreamPlatformDetailView.as_view(), name='platform-detail'),    
    path('stream/<int:pk>/review-create/', ReviewCreateView.as_view(), name='review-create'), 
    path('stream/<int:pk>/review/', ReviewListView.as_view(), name='review-list'), 
    path('stream/review/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
    path('api-auth/logout/', LogoutView.as_view(), name='logout'),
]
