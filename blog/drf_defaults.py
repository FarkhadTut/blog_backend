from rest_framework.pagination import PageNumberPagination


class MyPaginator(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'limit'
    max_page_size = 50