# myapp/serializers.py
from rest_framework import serializers
from car.models import vehicle_info, vehicle_type_tab, vehicle_accessory_tab

class VehicleAccessorySerializer(serializers.ModelSerializer):
    class Meta:
        model = vehicle_accessory_tab
        fields = ['id', 'accessory_name', 'price']

class VehicleInfoSerializer(serializers.ModelSerializer):
    # accessories = VehicleAccessorySerializer(many=True, read_only=True)
    # accessory_count = serializers.SerializerMethodField()
    # total_accessory_price = serializers.SerializerMethodField()
    # type_name = serializers.SerializerMethodField()
    #
    # class Meta:
    #     model = vehicle_info
    #     fields = [
    #         'id', 'vehicle_name', 'year', 'price', 'type_name',
    #         'description', 'accessories', 'accessory_count', 'total_accessory_price'
    #     ]
    #
    # def get_accessory_count(self, obj):
    #     return obj.accessories.count()
    #
    # def get_total_accessory_price(self, obj):
    #     return sum(accessory.price for accessory in obj.accessories.all())
    #
    # def get_type_name(self, obj):
    #     type_obj = vehicle_type_tab.objects.filter(vehicle_id=obj.id).first()
    #     return type_obj.type_name if type_obj else None

    vehicleName = serializers.CharField(source='vehicle_name')
    type = serializers.CharField()  # 注：你需要 annotate 出来
    accessoryCount = serializers.IntegerField()
    totalAccessoryPrice = serializers.FloatField()

    class Meta:
        model = vehicle_info
        fields = ['id', 'vehicleName', 'year', 'price', 'type', 'accessoryCount', 'totalAccessoryPrice']

