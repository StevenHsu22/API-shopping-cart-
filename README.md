# 購物車 API 試作專案

### 資料庫架構

![](https://github.com/StevenHsu22/API_shoppingcart/blob/main/Api_picture/sql%E6%9E%B6%E6%A7%8B.png)


利用 Python Flask 建立購物車 API 串接 MySQL，並規劃 DB 架構，共設計七項 API，並撰寫在 swagger 文件。
1.設計 Signin API，提供註冊功能。
2.設計 Login API，執行登入功能，並加入 jwt_token。
3.使用 GET 取得所有商品資訊。
4.使用 GET 提供使用者可模糊搜尋產品的功能。
5.採用 POST 將商品放入購物車，並能同時檢查庫存是否足夠與算出購物車內的價錢。
6.利用 PATCH 新增或減少購物車內的商品，且也能檢查庫存是否足夠與算出購物車內的價錢。
7.利用 DELETE 刪除購物車商品,，並核對與回傳回庫存。
