from marshmallow import Schema, fields


class UserGetSchema(Schema):
    name = fields.Str(example="string")

# Parameter (Schema)
class UserPostSchema(Schema):
    product_name = fields.Str(doc="product_name", example="string", required=True)
    user_id = fields.Int(doc="user_id", example="int", required=True)
    amount = fields.Int(doc="amount", example="int", required=True)
    # account = fields.Str(doc="account", example="string", required=True)
    # password = fields.Str(doc="password", example="string", required=True)



class UserPatchSchema(Schema):
    product_name = fields.Str(doc="product_name", example="string")
    order_id = fields.Int(doc="order_id", example="int")
    amount = fields.Int(doc="amount", example="int")
    # account = fields.Str(doc="account", example="string")
    # password = fields.Str(doc="password", example="string")

# Common
class UserCommonResponse(Schema):
    message = fields.Str(example="success")

class UserPostResponse(UserPostSchema):
    total_price = fields.Int(example={"total_price": 0})

# Get
class UserGetResponse(UserCommonResponse):
    datatime = fields.Str(example="1970-01-01T00:00:00.000000")
    name = fields.Str(doc="product_name", example="string")
    data = fields.List(fields.Dict(), example={
        "id": 0,
        "name": "name",
        "price": 0,
        "amount": 0
    })


#密碼
class LoginSchema(Schema):
    account = fields.Str(doc="account", example="string", required=True)
    password = fields.Str(doc="password", example="string", required=True)

#註冊
class SignSchema(Schema):
    name = fields.Str(doc="name", example="string", required=True)
    account = fields.Str(doc="account", example="string", required=True)
    password = fields.Str(doc="password", example="string", required=True)