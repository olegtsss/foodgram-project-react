from rest_framework.pagination import PageNumberPagination
from django.conf import settings


class CustomPagination(PageNumberPagination):
    """
    Собственный пагинатор.
    Client can control the page size using <page_size_query_param>.
    """

    page_size_query_param = 'limit'
    page_size = settings.PAGE_SIZE
