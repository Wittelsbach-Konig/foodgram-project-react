from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """
    Кастомный пагинатор для изменения
    объектов на страницы с помощью limit.
    """

    page_size_query_param = 'limit'
