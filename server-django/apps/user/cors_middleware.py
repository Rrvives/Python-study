"""
开发期 CORS：允许浏览器 SPA 跨域访问 /api/*。
生产环境建议改用 django-cors-headers 并收紧 Allow-Origin。
"""
from django.http import HttpResponse


class AllowApiCorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/api/") and request.method == "OPTIONS":
            resp = HttpResponse(status=204)
            self._apply(resp)
            return resp

        response = self.get_response(request)
        if request.path.startswith("/api/"):
            self._apply(response)
        return response

    @staticmethod
    def _apply(response: HttpResponse) -> None:
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Headers"] = (
            "Content-Type, Authorization, X-Auth-Username"
        )
        response["Access-Control-Allow-Methods"] = (
            "GET, POST, PATCH, PUT, DELETE, OPTIONS"
        )
