from rest_framework.pagination import PageNumberPagination


class NewPageNumberPaginator(PageNumberPagination):
    page_size_query_param = 'limit'
