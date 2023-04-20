from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView


class WrappedResponseDataMixin(APIView):
    """
    response data를 아래와 같은 포맷으로 wrapping 합니다
    {
        "meta": {
            "code": int,
            "message": str or dict,
        },
        "data": data,
    }
    """

    def get_response_message(self, code, data):
        if status.is_success(code):
            return "ok"
        if status.is_client_error(code):
            return JSONRenderer().render(data)
        if status.is_server_error(code):
            return "server error"

    def get_response_data(self, code, data):
        if status.is_client_error(code) or status.is_server_error(code):
            return None
        return data

    def wrap_data(self, response):
        code = response.status_code
        data = response.data

        if code == status.HTTP_204_NO_CONTENT:
            return response

        return {
            "meta": {
                "code": code,
                "message": self.get_response_message(code, data),
            },
            "data": self.get_response_data(code, data),
        }

    def finalize_response(self, request, response, *args, **kwargs):
        response.data = self.wrap_data(response)
        return super().finalize_response(request, response, *args, **kwargs)
