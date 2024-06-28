from rest_framework import status 
from rest_framework import mixins 
from rest_framework import generics
from django.shortcuts import redirect
from django.contrib.auth import logout
from rest_framework import permissions
from rest_framework.views import APIView 
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError 
from watchlist.models import WatchList, StreamPlatform, Review
from watchlist.throttling import ReviewCreateThrottle, ReviewListThrottle
from watchlist.permissions import AdminOrReadOnly, ReviewAuthorOrReadOnly # Custom permissions 
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle # Throttling
from watchlist.serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer

from django_filters.rest_framework import DjangoFilterBackend # Filtering
from rest_framework import filters # Searching
from watchlist.pagination import WatchListPagination, WatchListLimitOffSet # Pagination for watchlist


class WatchListView(generics.ListCreateAPIView):
    """
    View for listing and creating movies.

    This view supports both retrieving a list of all movies and creating a new movie entry.

    Attributes:
        serializer_class: The serializer class for Movie objects.
    """
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    pagination_class = WatchListLimitOffSet

class MovieDetailView(APIView):
    """
    View for retrieving, updating, or deleting a movie.

    This view supports retrieving details, updating, and deleting a specific movie.

    Attributes:
        serializer_class: The serializer class for Movie objects.
    """
    serializer_class = WatchListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        
    def get(self, request, pk):
        """
        Retrieve details of a specific movie.

        Args:
            request: HTTP request object.
            pk: Primary key of the movie to retrieve.

        Returns:
            Response: Serialized movie data as a JSON response or an error response in case of a not found exception.
        """
        movie = get_object_or_404(WatchList, pk=pk)
        serializer = self.serializer_class(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """
        Update details of a specific movie.

        Args:
            request: HTTP request object.
            pk: Primary key of the movie to update.

        Returns:
            Response: Serialized movie data as a JSON response after update or an error response in case of validation failure.
        """
        movie = get_object_or_404(WatchList, pk=pk)
        serializer = self.serializer_class(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a specific movie.

        Args:
            request: HTTP request object.
            pk: Primary key of the movie to delete.

        Returns:
            Response: A success response indicating the movie has been deleted.
        """
        movie = get_object_or_404(WatchList, pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)       
    
class StreamPlatformListView(APIView):
    """
    API endpoint for listing and creating stream platforms.

    GET:
    Retrieve a list of all stream platforms.

    POST:
    Create a new stream platform.
    """
    serializer_class = StreamPlatformSerializer

    def get(self, request):
        """
        Retrieve a list of all stream platforms.

        Returns:
            Response: A JSON response containing a list of stream platforms.
        """
        queryset = StreamPlatform.objects.all()
        serializer = self.serializer_class(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new stream platform.

        Args:
            request: The HTTP request object.

        Returns:
            Response: A JSON response with the created stream platform or validation errors.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StreamPlatformDetailView(APIView):
    """
    API endpoint for retrieving, updating, and deleting a specific stream platform.

    GET:
    Retrieve a specific stream platform.

    PUT:
    Update a specific stream platform.

    DELETE:
    Delete a specific stream platform.
    """
    serializer_class = StreamPlatformSerializer

    def get(self, request, pk):
        """
        Retrieve a specific stream platform.

        Args:
            request: The HTTP request object.
            pk: The primary key of the stream platform.

        Returns:
            Response: A JSON response containing the stream platform details.
        """
        platform = get_object_or_404(StreamPlatform, pk=pk)
        serializer = self.serializer_class(platform,context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """
        Update a specific stream platform.

        Args:
            request: The HTTP request object.
            pk: The primary key of the stream platform.

        Returns:
            Response: A JSON response with the updated stream platform or validation errors.
        """
        platform = get_object_or_404(StreamPlatform, pk=pk)
        serializer = self.serializer_class(platform,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a specific stream platform.

        Args:
            request: The HTTP request object.
            pk: The primary key of the stream platform.

        Returns:
            Response: An empty JSON response with a 204 No Content status.
        """
        platform = get_object_or_404(StreamPlatform, pk=pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ReviewCreateView(generics.CreateAPIView):
    """
    API endpoint for creating a new review for a specific WatchList.

    POST:
    Create a new review for the specified WatchList.
    """
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        """
        Perform the creation of a new review.

        Args:
            serializer: The serializer instance.

        Returns:
            None
        """
        watchlist_pk = self.kwargs['pk']
        watchlist = WatchList.objects.get(pk=watchlist_pk)
        
        user = self.request.user
        review = Review.objects.filter(watchlist=watchlist, user=user)
        
        if review.exists():
            raise ValidationError('You have already reviewed this watchlist.')
        
        new_rating = serializer.validated_data['rating']
        total_rating = watchlist.average_rating * watchlist.number_of_rating
        total_rating += new_rating
        watchlist.number_of_rating += 1
        watchlist.average_rating = total_rating / watchlist.number_of_rating
        
        watchlist.save() 
        serializer.save(watchlist=watchlist, user=user)
    
class ReviewListView(generics.ListAPIView):
    """
    API endpoint for listing and creating reviews related to a specific WatchList.

    GET:
    Retrieve a list of reviews for a specific WatchList.

    POST:
    Create a new review for a specific WatchList.
    """
    serializer_class = ReviewSerializer
    permission_classes = [ReviewAuthorOrReadOnly]
    throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user__username', 'active']

    def get_queryset(self):
        """
        Get the queryset of reviews for a specific WatchList.

        Returns:
            QuerySet: Reviews related to the specified WatchList.
        """
        watchlist_pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=watchlist_pk)
    
    
class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewAuthorOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'
    

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        logout(request)
        return redirect('/')

