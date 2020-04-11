from rest_framework.pagination import PageNumberPagination


class RateResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_query_param = 'page'
