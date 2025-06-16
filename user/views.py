from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from django.utils.decorators import method_decorator
from django.views import View
from user.models import Sysuser, SysuserSerializer
from rest_framework_jwt.settings import api_settings
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
# @method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    def post(self, request):
        try:
            username = Sysuser.objects.get(username=request.data.get('username'))
        except:
            return JsonResponse({"message": "用户不存在", "code": 400, "data": []})
        return JsonResponse({"message": "Hello World", "code": 200, "user": SysuserSerializer(username).data})


class TestView(View):
    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if token != None and token != '':
            print(token, 'token')
            userList = Sysuser.objects.all()
            print(userList, 'userList', type(userList))
            userList_dict = userList.values()
            print(userList_dict, "userList_dict", type(userList_dict))
            userListData = list(userList_dict)
            print(userListData, "userListData", type(userListData))
            return JsonResponse({"message": "Hello World", "code": 200, "data": userListData})
        else:
            return JsonResponse({"message": "Hello World", "code": 401, "data": []})


class JwtTestView(View):
    # 模拟token
    def get(self, request):
        user = Sysuser.objects.get(username="user1")
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        jwt_payload = jwt_payload_handler(user)
        token = jwt_encode_handler(jwt_payload)
        return JsonResponse({"message": "Hello World", "code": 200, "token": token})
