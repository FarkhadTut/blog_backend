from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status


class MyPaginator(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'limit'
    max_page_size = 50

    def get_paginated_response(self, data):
        response = Response({
            'links': {
               'next': self.get_next_link(),
               'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'results': data
        }, status=status.HTTP_200_OK)


        return response