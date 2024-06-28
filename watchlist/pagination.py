from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

class WatchListPagination(PageNumberPagination):
    page_size = 5
    page_query_param = "PageNumber" # Changing the name of param for page_size in url
    page_size_query_param = 'dataSize' # Render the data according to your number that you wish
    max_page_size = 5 # This is will restrict to reder the data more than 5 entries

class WatchListLimitOffSet(LimitOffsetPagination):
    default_limit = 5
