# Watchlist API

## Overview

The Watchlist API is a Django-based project that provides endpoints for managing movies, stream platforms, and reviews. It leverages the Django REST framework for building robust and scalable RESTful APIs. The API supports functionalities like listing, creating, updating, and deleting movies and stream platforms, as well as creating and managing reviews.

## Features

- **Movies**: Create, retrieve, update, and delete movie records.
- **Stream Platforms**: Manage stream platforms, including listing and creating new platforms.
- **Reviews**: Users can create, list, update, and delete reviews for movies.
- **Authentication**: Token-based authentication for secure access.
- **Permissions**: Custom permission classes to manage access control.
- **Throttling**: Rate limiting to prevent abuse of the API.
- **Filtering and Searching**: Easily filter and search through movie and review records.
- **Pagination**: Efficient handling of large datasets with pagination support.

## Technologies Used

- **Django**: High-level Python web framework that encourages rapid development.
- **Django REST framework**: Powerful and flexible toolkit for building Web APIs.
- **PostgreSQL**: Advanced SQL database used for data storage.
- **JWT (JSON Web Tokens)**: Secure token-based authentication mechanism.
- **Django Filters**: Simplifies adding filters to Django REST framework views.
- **Throttling**: Implements rate limiting to prevent abuse of API endpoints.

## Implementation Details

### Models

The application defines three main models:

- **WatchList**: Represents a movie with attributes like title, storyline, platform, and rating details.
- **StreamPlatform**: Represents a streaming platform with attributes like name, about, and website.
- **Review**: Represents a review for a movie with attributes like user, rating, description, and watchlist reference.

### Serializers

Serializers are used to convert complex data types, such as querysets and model instances, into native Python data types that can then be easily rendered into JSON or XML. The serializers defined include:

- **WatchListSerializer**
- **StreamPlatformSerializer**
- **ReviewSerializer**

### Views

The views handle HTTP requests and responses. The key views include:

- **WatchListView**: Handles listing and creating movie entries.
- **MovieDetailView**: Handles retrieving, updating, and deleting a specific movie.
- **StreamPlatformListView**: Manages listing and creating stream platforms.
- **StreamPlatformDetailView**: Handles retrieving, updating, and deleting a specific stream platform.
- **ReviewCreateView**: Allows authenticated users to create reviews for movies.
- **ReviewListView**: Lists reviews related to a specific movie.
- **ReviewDetailView**: Manages retrieving, updating, and deleting a specific review.
- **LogoutView**: Logs out the authenticated user.

### Permissions and Throttling

Custom permission classes ensure that only authorized users can perform certain actions:

- **AdminOrReadOnly**: Allows full access to admin users, read-only access to others.
- **ReviewAuthorOrReadOnly**: Only the author of a review or an admin can modify it.

Throttling is implemented to control the rate of requests:

- **ReviewCreateThrottle**: Limits the rate of creating new reviews.
- **ReviewListThrottle**: Limits the rate of listing reviews.
- **ScopedRateThrottle**: Applies throttling to specific views, such as review details.

### Filtering, Searching, and Pagination

- **Filtering**: Implemented using `DjangoFilterBackend` to filter reviews by username and status.
- **Searching**: Enabled through `filters.SearchFilter` for searching movies by title.
- **Pagination**: Custom pagination classes (`WatchListPagination` and `WatchListLimitOffSet`) are used to manage large datasets efficiently.

## Getting Started

### Prerequisites

- Python 3.8+
- Django 3.1+
- Django REST framework
- PostgreSQL

### Installation

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up PostgreSQL database and update `settings.py` with database credentials.

4. Run migrations:
    ```bash
    python manage.py migrate
    ```

5. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```

6. Start the development server:
    ```bash
    python manage.py runserver
    ```

### Testing

Run the test suite to ensure everything is working correctly:
```bash
python manage.py test
