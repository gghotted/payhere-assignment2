from functools import partial

from schema import Or, Schema


def _res_schema(code, data=None):
    return Schema(
        {
            "meta": {
                "code": code,
                "message": str,
            },
            "data": data,
        }
    )


def cursor_pagination_schema(data_schema: Schema):
    return Schema(
        {
            "next": Or(str, None),
            "previous": Or(str, None),
            "results": [data_schema],
        }
    )


res200_schema = partial(_res_schema, 200)
res201_schema = partial(_res_schema, 201)
res400_schema = _res_schema(400, data=None)
res401_schema = _res_schema(401, data=None)
res403_schema = _res_schema(403, data=None)
res404_schema = _res_schema(404, data=None)


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

store_schema = Schema(
    {
        "id": int,
        "owner": int,
        "name": str,
    }
)

category_schema = Schema(
    {
        "id": int,
        "store": int,
        "name": str,
    }
)

product_schema = Schema(
    {
        "id": int,
        "store": int,
        "category_name": str,
        "price": int,
        "cost": int,
        "name": str,
        "chosung": str,
        "description": str,
        "barcode": str,
        "sell_by_days": int,
        "size": str,
    }
)
