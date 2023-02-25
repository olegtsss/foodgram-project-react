from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """
    Собственный пагинатор.
    Client can control the page size using <page_size_query_param>.
    """

    page_size_query_param = 'limit'
    page_size = 50
