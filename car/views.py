from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, filters, status
from rest_framework.parsers import JSONParser
from django.db import transaction
from django.db.models import F
from car.models import vehicle_info, vehicle_type_tab, vehicle_accessory_tab
from .serializers import VehicleInfoSerializer
from .pagination import VehiclePagination


# 添加数据
class AddVehicleView(APIView):
    parser_classes = [JSONParser]
    def post(self, request):
        data = request.data
        try:
            with transaction.atomic():
                vehicle = vehicle_info.objects.create(
                    vehicle_name=data['vehicle_name'],
                    year=data['year'],
                    price=data['price'],
                    description=data.get('description', '')
                )
                vehicle_type_tab.objects.create(
                    vehicle_id=vehicle.id,
                    type_name=data['type_name']
                )
                for accessory in data.get('accessories', []):
                    vehicle_accessory_tab.objects.create(
                        vehicle_id=vehicle.id,
                        accessory_name=accessory['name'],
                        price=accessory['price']
                    )
            return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# 分页筛选数据
class VehicleListView(generics.ListAPIView):
    queryset = vehicle_info.objects.all()
    serializer_class = VehicleInfoSerializer
    pagination_class = VehiclePagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['vehicle_name', 'year']

    def get_queryset(self):
        queryset = super().get_queryset()
        vehicle_name = self.request.query_params.get('vehicle_name', '')
        year = self.request.query_params.get('year', '')
        if vehicle_name:
            queryset = queryset.filter(vehicle_name__icontains=vehicle_name)
        if year:
            queryset = queryset.filter(year__icontains=year)
        return queryset.prefetch_related('accessories')

# 更新指定的字段
class UpdateVehiclePricesView(APIView):
    def post(self, request):
        try:
            with transaction.atomic():
                # 从请求中读取参数
                target_name = request.data.get('vehicle_name', 'CarB')
                target_price = float(request.data.get('target_price', 130000.0))
                increase_amount = float(request.data.get('increase_amount', 5000.0))
                block_year = int(request.data.get('block_year', 2019))

                # 保存初始价格（如果你打算用于日志或回滚处理）
                initial_prices = list(vehicle_info.objects.all().values('id', 'price'))
                initial_accessory_prices = list(vehicle_accessory_tab.objects.all().values('id', 'price'))

                # 更新价格
                vehicle_info.objects.filter(vehicle_name=target_name).update(price=target_price)
                vehicle_info.objects.exclude(vehicle_name=target_name).update(price=F('price') + increase_amount)

                # 校验不符合要求的记录
                vehicles_to_check = vehicle_info.objects.filter(year__lt=block_year, price__gte=target_price)
                if vehicles_to_check.exists():
                    raise ValueError(f"存在年份早于 {block_year} 且价格高于 {target_price} 的车辆，禁止操作。")

                return Response({'status': 'success'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# 条件删除
class DeleteVehiclesView(APIView):
    def post(self, request):
        try:
            with transaction.atomic():
                # 从请求中获取年份参数
                delete_before_year = int(request.data.get('year', 2019))

                vehicles_to_delete = vehicle_info.objects.filter(year__lt=delete_before_year)
                vehicle_ids = list(vehicles_to_delete.values_list('id', flat=True))

                vehicle_type_tab.objects.filter(vehicle_id__in=vehicle_ids).delete()
                vehicle_accessory_tab.objects.filter(vehicle_id__in=vehicle_ids).delete()
                vehicles_to_delete.delete()

                return Response({'status': 'success'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
