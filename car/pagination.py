from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
class VehiclePagination(PageNumberPagination):
    # page_query_param = 'pageNo'  # 页码参数名
    # page_size_query_param = 'pageSize'  # 每页大小参数名
    # max_page_size = 100
    # page_size = 10

    page_query_param = 'pageNo'
    page_size_query_param = 'pageSize'

    def get_paginated_response(self, data):
        return Response({
            'data': data,
            'total': self.page.paginator.count,
            'pageNo': self.page.number,
            'pageSize': self.get_page_size(self.request),
        })