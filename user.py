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
        expires_delta=timedelta(days=10) #期限10天
    )
    return token 

class Search_all(MethodResource):
    #顯示產品資訊
    @doc(description='Get all products info.', tags=['Search products'])
    @marshal_with(UserGetResponse, code=200)
    @jwt_required()
    def get(self):
        db, cursor = db_init()

        sql = """

            SELECT * FROM api_class.product;

        """
        cursor.execute(sql)

        users = cursor.fetchall()
        db.close()
        return util.success(users)
     
class Users(MethodResource):
    #放入購物車&呈現購物車商品+總金額
    @doc(description='add products to cart.', tags=['Shopping Cart'])
    @use_kwargs(UserPostSchema,location="json")
    @marshal_with(UserPostResponse, code=201)
    @jwt_required()
    def post(self, **kwargs):
        db, cursor = db_init()

        user = {
            'product_name': kwargs['product_name'],
            'user_id': int(kwargs['user_id']),
            'amount': int(kwargs['amount'])
        }

        #查詢商品庫存是否足夠
        sql_product = f"SELECT * FROM api_class.product WHERE name = '{user['product_name']}';"
        cursor.execute(sql_product)
        
        result_product = cursor.fetchall()
        if result_product == ():
            db.close()
            return ({"message": "product is not exist"})

        if result_product[0]['amount'] < user['amount']:
            db.close()
            return ({"message": "product is not enough now"})

        sql = """

            INSERT INTO `api_class`.`cart` (`product_name`,`user_id`,`amount`)
            VALUES ('{}','{}','{}');

        """.format(user['product_name'], user['user_id'], user['amount'])

        result = cursor.execute(sql)
        db.commit()

        product_stock = result_product[0]['amount'] - user['amount']

        sql_stock = """

            UPDATE api_class.product
            SET amount = {}
            WHERE name = '{}';

        """.format(product_stock, user['product_name'])

        cursor.execute(sql_stock)
        db.commit()

        sql_items = """

            SELECT order_id, product_name, amount FROM api_class.cart 
            where cart.user_id = '{}';

        """.format(user['user_id'])

        cursor.execute(sql_items)
        db.commit()
        items = cursor.fetchall()

        sql2 = """

            SELECT sum(cart.amount*product.price) as sum FROM `cart`,`product` 
            where cart.product_name = product.name and cart.user_id = '{}';

        """.format(user['user_id'])
   
        cursor.execute(sql2)
        db.commit()
        total_price = cursor.fetchone()

        db.commit()
        db.close()
        
        if result == 1:
            return util.success(items, total_price['sum'])
        else:
            return util.failure()
    
class Search(MethodResource):
    #模糊搜尋產品
    @doc(description='Get products info.', tags=['Search products'])
    @use_kwargs(UserGetSchema,location="json")
    @marshal_with(UserGetResponse, code=200)
    @jwt_required()
    def get(self, **kwargs):
        db, cursor = db_init() 
        user = {
            'name': kwargs.get("name")
        }
        
        sql = """

            SELECT * FROM api_class.product where name like '%{}%';

        """.format(user['name'])

        cursor.execute(sql)
        print(user)
        users = cursor.fetchall()
        db.commit()
        db.close()
        return util.success(users)



class User(MethodResource):
    #調整購物車產品
    @doc(description='alter cart products.', tags=['Shopping Cart'])
    @use_kwargs(UserPatchSchema,location="json")
    @marshal_with(UserPostResponse, code=201)
    @jwt_required()
    def patch(self, id, **kwargs):
        db, cursor = db_init()
        
        user = {
            'order_id': kwargs.get('order_id'),
            'product_name': kwargs.get('product_name'),
            'amount': int(kwargs.get('amount'))
        }

        #查詢商品庫存是否足夠
        sql_product = f"SELECT * FROM api_class.product WHERE name = '{user['product_name']}';"
        cursor.execute(sql_product)
        db.commit()
        
        result_product = cursor.fetchall()

        if result_product[0]['amount'] < user['amount']:
            db.close()
            return ({"message": "product is not enough now"})


        #判斷回傳庫存的數值
        sql_search_product = f"SELECT * FROM api_class.cart WHERE order_id = '{user['order_id']}';"
        cursor.execute(sql_search_product)
        db.commit()
        result_search_product = cursor.fetchall()
        
        if result_search_product[0]['amount'] > user['amount']:
            product_stock = result_search_product[0]['amount'] - user['amount']
        else:
            product_stock = result_search_product[0]['amount'] - user['amount']

        sql_stock = """

            UPDATE api_class.product
            SET amount = amount + {}
            WHERE name = '{}';

        """.format(product_stock, user['product_name'])

        cursor.execute(sql_stock)
        db.commit()

        query = []
        print(user)
        '''{'product_name': 'None', 'amount': None}'''
        for key, value in user.items():
            if value is not None and key != 'order_id':
                query.append(f"{key} = '{value}'")
        query = ",".join(query)
        '''
        UPDATE table_name
        SET column1=value1, column2=value2, column3=value3···
        WHERE some_column=some_value;

        '''
        sql = """

            UPDATE api_class.cart
            SET {}
            WHERE cart.order_id = {} and cart.user_id = {} ;

        """.format(query, user['order_id'], id)

        result = cursor.execute(sql)
        db.commit()

        sql_items = """

            SELECT order_id, product_name, amount FROM api_class.cart 
            where cart.user_id = '{}';

        """.format(id)

        cursor.execute(sql_items)
        db.commit()
        items = cursor.fetchall()

        sql2 = """

            SELECT sum(cart.amount*product.price) as sum FROM `cart`,`product` 
            where cart.product_name = product.name and cart.user_id = '{}';

        """.format(id)
   
        cursor.execute(sql2)
        db.commit()
        total_price = cursor.fetchone()

        db.close()
        
        if result == 1:
            return util.success(items, total_price['sum'])
        else:
            return util.failure()

class Delete(MethodResource):
    #刪除購物車產品    
    @doc(description='Delete cart items.', tags=['Shopping Cart'])
    @marshal_with(UserCommonResponse, code=201)
    @jwt_required()
    def delete(self, user_id, order_id):
        db, cursor = db_init()

        #刪除前核對並回傳庫存
        sql_cart_product = f'SELECT * FROM `api_class`.`cart` WHERE order_id = {order_id};'
        cursor.execute(sql_cart_product)
        db.commit()
        result_cart_product = cursor.fetchall()

        sql_delete = """

            UPDATE api_class.product
            SET amount = amount + {}
            WHERE name = '{}';

        """.format(result_cart_product[0]['amount'], result_cart_product[0]['product_name'])

        cursor.execute(sql_delete)
        db.commit()

        sql = f'DELETE FROM `api_class`.`cart` WHERE user_id = {user_id} and order_id = {order_id};'
        result = cursor.execute(sql)

        sql_items = """

            SELECT order_id, product_name, amount FROM api_class.cart 
            where cart.user_id = '{}';

        """.format(user_id)

        cursor.execute(sql_items)
        db.commit()
        items = cursor.fetchall()

        sql2 = """

            SELECT sum(cart.amount*product.price) as sum FROM `cart`,`product` 
            where cart.product_name = product.name and cart.user_id = '{}';

        """.format(user_id)
   
        cursor.execute(sql2)
        db.commit()
        total_price = cursor.fetchone()

        db.close()

        if result == 1:
            return util.success(items, total_price['sum'])
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

        sql_account = """

            SELECT * FROM api_class.user;

        """
        cursor.execute(sql_account)
        result_account = cursor.fetchall()
        db.commit()

        if result_account[0]['account'] == user['account']:
            db.close()
            return ({"message": "account is exist, please change another one"})

        
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