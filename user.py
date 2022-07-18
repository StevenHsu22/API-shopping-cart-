from flask_restful import reqparse
import pymysql
from flask import jsonify
import util
from flask_apispec import doc, use_kwargs, MethodResource, marshal_with
from user_router_model import *
from flask_jwt_extended import create_access_token, jwt_required
from datetime import timedelta

def db_init(): 
    db = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        port=3306,
        db='api_class'
    )
    cursor = db.cursor(pymysql.cursors.DictCursor)
    return db, cursor

def get_access_token(account):
    token = create_access_token(
        identity={"account": account},
        expires_delta=timedelta(days=1)
    )
    return token 

class Users(MethodResource):
    @doc(description='Get products info.', tags=['User'])
    @marshal_with(UserGetResponse, code=200)
    @jwt_required()
    def get(self):
        db, cursor = db_init()

        sql = "SELECT * FROM api_class.product;"
        cursor.execute(sql)

        users = cursor.fetchall()
        db.close()
        return util.success(users)

    @doc(description='add products to cart.', tags=['User'])
    @use_kwargs(UserPostSchema,location="json")
    @marshal_with(UserCommonResponse, code=200)
    def post(self, **kwargs):
        db, cursor = db_init()

        user = {
            'product_id': int(kwargs['product_id']),
            'user_id': int(kwargs['user_id']),
            'amount': int(kwargs['amount'])
        }
        sql = """

        INSERT INTO `api_class`.`cart` (`product_id`,`user_id`,`name`,`amount`)
        VALUES ('{}','{}', name = (select name from product where cart.user_id = product.id),'{}');

        """.format(user['product_id'], user['user_id'], user['amount'])

        result = cursor.execute(sql)

        db.commit()
        db.close()
        
        if result == 1:
            return util.success()
        else:
            return util.failure()
    
    

class User(MethodResource):
    @doc(description='alter cart products.', tags=['User'])
    @use_kwargs(UserPatchSchema,location="json")
    @marshal_with(UserCommonResponse, code=200)
    def patch(self, id, **kwargs):
        db, cursor = db_init()
        
        user = {
            'product_id': int(kwargs.get('product_id')),
            'user_id': int(kwargs.get('user_id')),
            'amount': int(kwargs.get('amount'))
        }

        query = []
        print(user)
        '''{'name': None, 'price': 'Double', 'amount': None}'''
        for key, value in user.items():
            if value is not None:
                query.append(f"{key} = '{value}'")
        query = ",".join(query)
        '''
        UPDATE table_name
        SET column1=value1, column2=value2, column3=value3···
        WHERE some_column=some_value;

        '''
        sql = """
            UPDATE api_class.product
            SET {}
            WHERE id = {};
        """.format(query, id)

        result = cursor.execute(sql)

        db.commit()
        db.close()
        
        if result == 1:
            return util.success()
        else:
            return util.failure()

    @doc(description='Delete users.', tags=['User'])
    @marshal_with(UserCommonResponse, code=200)
    def delete(self, id):
        db, cursor = db_init()
        sql = f'DELETE FROM `api_class`.`product` WHERE id = {id};'
        result = cursor.execute(sql)

        db.commit()
        db.close()

        if result == 1:
            return util.success()
        else:
            return util.failure()

class Login(MethodResource):
    @doc(description='User Login', tags=['Login'])
    @use_kwargs(LoginSchema, location="json")
    # @marshal_with(user_router_model.UserGetResponse, code=200)
    def post(self, **kwargs):
        db, cursor = db_init()
        account, password = kwargs["account"], kwargs["password"]
        sql = f"SELECT * FROM api_class.user WHERE account = '{account}' AND password = '{password}';"
        cursor.execute(sql)
        user = cursor.fetchall() #如果是空值會回傳 ()
        db.close()

        if user != ():
            token = get_access_token(account)
            data = {
                "message": f"Welcome back {user[0]['name']}",
                "token": token}
            return util.success(data)
        
        return util.failure({"message":"Account or password is wrong"})


class Sign(MethodResource):
    @doc(description='User Sign', tags=['Signin'])
    @use_kwargs(SignSchema,location="json")
    @marshal_with(UserCommonResponse, code=200)
    def post(self, **kwargs):
        db, cursor = db_init()

        user = {
            'name': kwargs['name'],
            'account': kwargs['account'],
            'password': kwargs['password']
        }
        sql = """

        INSERT INTO `api_class`.`user` (`name`,`account`,`password`)
        VALUES ('{}','{}','{}');

        """.format(user['name'], user['account'], user['password'])

        result = cursor.execute(sql)

        db.commit()
        db.close()
        
        if result == 1:
            return util.success()
        else:
            return util.failure()