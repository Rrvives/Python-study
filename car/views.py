from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, filters, status
from rest_framework.parsers import JSONParser
from django.db import transaction
from django.db.models import F
from django.db.models import Count, Sum, FloatField
from django.db.models.functions import Coalesce
from django.db.models import OuterRef, Subquery
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

    def get_queryset(self):
        queryset = vehicle_info.objects.all()
        params = self.request.query_params

        keyword = params.get('keyword')
        if keyword:
            queryset = queryset.filter(vehicle_name__icontains=keyword)

        min_year = params.get('minYear')
        if min_year:
            queryset = queryset.filter(year__gte=min_year)

        max_year = params.get('maxYear')
        if max_year:
            queryset = queryset.filter(year__lte=max_year)

        min_price = params.get('minPrice')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        # 注入车辆类型
        type_subquery = vehicle_type_tab.objects.filter(vehicle_id=OuterRef('pk')).values('type_name')[:1]

        queryset = queryset.annotate(
            type=Subquery(type_subquery),
            accessoryCount=Count('accessories'),
            totalAccessoryPrice=Coalesce(Sum('accessories__price', output_field=FloatField()), 0.0)
        )

        return queryset

# 更新指定的字段
class UpdateVehiclePricesView(APIView):
    def post(self, request):
        try:
            with transaction.atomic():
                target_name = request.data.get('vehicle_name', 'CarB')
                target_price = float(request.data.get('target_price', 130000.0))
                increase_amount = float(request.data.get('increase_amount', 5000.0))
                block_year = int(request.data.get('block_year', 2019))
                initial_prices = list(vehicle_info.objects.all().values('id', 'price'))
                initial_accessory_prices = list(vehicle_accessory_tab.objects.all().values('id', 'price'))
                vehicle_info.objects.filter(vehicle_name=target_name).update(price=target_price)
                vehicle_info.objects.exclude(vehicle_name=target_name).update(price=F('price') + increase_amount)
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
                delete_before_year = int(request.data.get('year', 2019))
                vehicles_to_delete = vehicle_info.objects.filter(year__lt=delete_before_year)
                vehicle_ids = list(vehicles_to_delete.values_list('id', flat=True))
                deleted_vehicles_count = vehicles_to_delete.count()
                deleted_types_count = vehicle_type_tab.objects.filter(vehicle_id__in=vehicle_ids).count()
                deleted_accessories_count = vehicle_accessory_tab.objects.filter(vehicle_id__in=vehicle_ids).count()
                vehicle_type_tab.objects.filter(vehicle_id__in=vehicle_ids).delete()
                vehicle_accessory_tab.objects.filter(vehicle_id__in=vehicle_ids).delete()
                vehicles_to_delete.delete()
                return Response({
                    "deletedVehicles": deleted_vehicles_count,
                    "deletedTypes": deleted_types_count,
                    "deletedAccessories": deleted_accessories_count
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
