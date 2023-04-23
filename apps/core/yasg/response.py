from .schemas import *


def _res(message, res_schema=None, data_schema=None):
    if res_schema and data_schema:
        res_schema = res_schema(data_schema)
    return Response(message, res_schema)


res200 = partial(_res, "성공", res200_schema)
res201 = partial(_res, "생성 성공", res201_schema)
res204 = _res("컨텐츠 없음")
res400 = _res("클아이언트 에러", res400_schema)
res401 = _res("인증 에러", res401_schema)
res403 = _res("권한 에러", res403_schema)
res404 = _res("찾을 수 없음", res404_schema)
