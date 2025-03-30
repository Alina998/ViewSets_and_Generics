from rest_framework.pagination import PageNumberPagination

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10  # Количество элементов на странице
    page_size_query_param = 'page_size'  # Параметр для указания размера страницы
    max_page_size = 100  # Максимально допустимый размер страницы