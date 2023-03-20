from django.conf import settings
from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """
    Собственный пагинатор.
    Client can control the page size using <page_size_query_param>.
    """

    # default -> page_query_param = 'page'
    page_size_query_param = 'limit'
    page_size = settings.PAGE_SIZE
