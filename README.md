# 購物車 API 試作專案

### 專案目標

利用 Python Flask 建立購物車 API 串接 MySQL，並規劃 DB 架構，共設計七項 API，並撰寫在 swagger 文件。

### 資料庫架構

* 整體架構

![](https://github.com/StevenHsu22/API_shoppingcart/blob/main/Api_picture/DB_schema.png)

主鍵: user.id, product.name, cart.order_id
外鍵: product.name -> cart.product_name, user.id -> cart.user_id

* phpadmin 設定

![](https://github.com/StevenHsu22/API_shoppingcart/blob/main/Api_picture/sql%E6%9E%B6%E6%A7%8B.png)

### 功能呈現(Postman)

1.設計 Signin API，提供註冊功能。

![](https://github.com/StevenHsu22/API_shoppingcart/blob/main/Api_picture/signin.png)

2.設計 Login API，執行登入功能，並加入 jwt_token。

![](https://github.com/StevenHsu22/API_shoppingcart/blob/main/Api_picture/login.png)

3.使用 GET 取得所有商品資訊。

![](https://github.com/StevenHsu22/API_shoppingcart/blob/main/Api_picture/search_all.png)

4.使用 GET 提供使用者可模糊搜尋產品的功能。

![](https://github.com/StevenHsu22/API_shoppingcart/blob/main/Api_picture/fuzzy_search.png)

5.採用 POST 將商品放入購物車，並能同時檢查庫存是否足夠與算出購物車內的價錢。

![](https://github.com/StevenHsu22/API_shoppingcart/blob/main/Api_picture/%E6%94%BE%E5%95%86%E5%93%81%E5%88%B0cart.png)

庫存不足and無商品的回傳

![](https://github.com/StevenHsu22/API_shoppingcart/blob/main/Api_picture/post%E5%BA%AB%E5%AD%98%E4%B8%8D%E8%B6%B3%E7%9A%84%E5%9B%9E%E5%82%B3.png)
![](https://github.com/StevenHsu22/API_shoppingcart/blob/main/Api_picture/post%E7%84%A1%E5%95%86%E5%93%81%E6%99%82%E7%9A%84%E5%9B%9E%E5%82%B3.png)

6.利用 PATCH 新增或減少購物車內的商品，且也能檢查庫存是否足夠與算出購物車內的價錢。

![](https://github.com/StevenHsu22/API_shoppingcart/blob/main/Api_picture/%E4%BF%AE%E6%94%B9cart%E5%95%86%E5%93%81.png)

庫存不足的回傳

![](https://github.com/StevenHsu22/API_shoppingcart/blob/main/Api_picture/patch%E5%BA%AB%E5%AD%98%E4%B8%8D%E8%B6%B3%E7%9A%84%E5%9B%9E%E5%82%B3.png)

7.利用 DELETE 刪除購物車商品,，並核對與回傳回庫存。

![](https://github.com/StevenHsu22/API_shoppingcart/blob/main/Api_picture/%E5%88%AA%E9%99%A4%E8%B3%BC%E7%89%A9%E8%BB%8A%E5%95%86%E5%93%81.png)
