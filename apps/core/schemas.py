from functools import partial

from schema import Or, Schema


def _res_schema(code, data=None):
    return Schema(
        {
            "meta": {
                "code": code,
                "message": Or(str, dict),
            },
            "data": data,
        }
    )


res200_schema = partial(_res_schema, 200)
res201_schema = partial(_res_schema, 201)
res400_schema = _res_schema(400, data=None)
res401_schema = _res_schema(401, data=None)
res403_schema = _res_schema(403, data=None)


user_schema = Schema(
    {
        "id": int,
        "phone": str,
    }
)

token_schema = Schema(
    {
        "access": str,
        "refresh": str,
    }
)
