from django.db import models

class vehicle_info(models.Model):
    # 定义字段
    vehicle_name = models.CharField(max_length=255, verbose_name='车辆名称')
    year = models.IntegerField(verbose_name='生产年份')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='车辆价格')
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name='介绍 & 备注')

    def __str__(self):
        return self.vehicle_name

    class Meta:
        verbose_name = '车辆信息'
        verbose_name_plural = '车辆信息'



class vehicle_type_tab(models.Model):
    # 定义字段
    vehicle_id = models.IntegerField(verbose_name='车辆 ID')
    type_name = models.CharField(max_length=255, verbose_name='车辆类型名称')

    def __str__(self):
        return self.type_name

    class Meta:
        verbose_name = '车辆类型'
        verbose_name_plural = '车辆类型'



class vehicle_accessory_tab(models.Model):
    vehicle = models.ForeignKey(vehicle_info, on_delete=models.CASCADE, related_name='accessories', verbose_name='车辆')
    accessory_name = models.CharField(max_length=255, verbose_name='配件名称')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='配件价格')

    def __str__(self):
        return self.accessory_name

    class Meta:
        verbose_name = '车辆配件'
        verbose_name_plural = '车辆配件'