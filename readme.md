

python flask : 前端 + 後端

Spark : 數據處理

MariaDB : 數據儲存 (Database)  + Flask-SQLAlchemy 的 ORM 框架

ML : KNN

參數有 : 

1. 訓練集 (可以 call sklean 內建的 buildin_wine、buildin_iris)
2. 要取幾個鄰居
3. Feature 的資料 column 數目



 ![AWS MLOps Framework | 參考架構圖](https://d1.awsstatic.com/Solutions/Solutions%20Category%20Template%20Draft/Solution%20Architecture%20Diagrams/AWS-MLOps-Framework.e8f367169c1c04f224501fb4858986b0eef1d9b2.jpg) 



# 如何使用

此 Proj 目前還沒完成，先說使用方式 : 
1. 環境建置 : 
   - 此 repo 提供的 docker-composer 可以建一個我用的，``docker-compose up``
     - 執行此指令請在英文目錄底下，因為因為他的 Name 會參照該目錄 ...
   - 在 Docker 內 / 或是你的電腦環境，可以先跑一次 ``pip install -r requirements.txt``
2. 如果只想 demo KNN with Spark，
  可以在有裝 Spark 的 Docker Container 內跑 (記得將 ``KNN()`` 取消註解)
  ``python final.py``
    - 其中，因為環境不同，可能得改一下  ``SPARK_HOME`` 的 path
    - 以及如果沒有下載 ``dis.txt``，想使用內建的 Lib，可以將 ``KNN()`` -> ``KNN('buildin_iris')``
3. 若想要 demo flask 的部分， ``python app.py``，然後去 ``localhost:5000`` 就能看到了。
  不過關於要串 KNN function 的話得把 flask 一起放到 docker 內執行，
  故暫時使用 ``test.py`` 代替，實際上並還沒實際測試過配合 ``final.py``
  總之打開網頁，然後輸入參數，他應該至少能正常的展示 POST Method。



待完成 : 

1. Query DB 可以給予欄位篩選
2. 提供更多對於 KNN 參數之調整
   - 可以上傳自己的 txt file



已知可能 bug :

1. 網頁端執行參數不可為空。
2. container 必須要有對應 port : ``-p 5678:5000``，
   且 container 內的 flask app 必須帶有參數 ``host='0.0.0.0'`` 才能正常在 host 吃到
   (這個參數已經在 code 中了，如果是用 docker-composer.xml build 也能內建 port 對應)



# 新增 DB 過程

```bash
apt install mariadb-server
#apt install systemd
/etc/init.d/mysql status
/etc/init.d/mysql start
mariadb -u root -p
create database traindb;
use traindb;
create table knn (
  Rid int AUTO_INCREMENT,
  Distance varchar(255),
  Score float,
  Neighbor int,
  DatasetName varchar(255),
  FeatureLen int,
  Time datetime
  PRIMARY KEY (Rid)
);
```

```
一些可能用到的指令
show columns from Knn
alter table Knn change column History Rid Integer primary key;
service mysql restart
alter table knn change Rid Rid int(11) AUTO_INCREMENT;
service mysql start
```



![](https://i.imgur.com/gygUVol.png)





```bash
pip install pymysql sqlalchemy
```

## 如果遇到 "Access denied for user 'root'@'localhost'"

- 最初我參考這篇 [ERROR 1698 (28000): Access denied for user 'root'@'localhost'](https://stackoverflow.com/questions/39281594/error-1698-28000-access-denied-for-user-rootlocalhost)
  - 裡面有提到，在 Debian 系統 'auth_socket' 會被稱為 'unix_socket'。
  - 我照做了一次，然後 root 就不能登入了 XD
    狀態碼改成 ``(1045, "Access denied for user 'root'@'localhost' (using password: YES)")``
- 遇到 (using password: YES) 這樣的，解決方式可以參考 [這篇](https://stackoverflow.com/questions/41818827/mysql-error-1045-access-denied-for-user-rootlocalhost-using-password/41821554)
  - 但很尷尬的是裡面並沒有教怎麼 start MySQL with --skip-grant-tables
    所以可以再參考 [這篇](https://stackoverflow.com/questions/1708409/how-to-start-mysql-with-skip-grant-tables)


## 如果遇到 "Table 'traindb.train_model' doesn't exist")"

在 Code 中，我的 Class 名稱叫做 train_model，
後來發現這個 Class Name 代表的就是 Table Name。

而當初在手動建立時，Table Name 叫做 Knn；
我將 Class 改成 Knn 了卻還是找不到 ...。

後來又發現，經過套件整合跑出來的指令都會是小寫，所以手動將 Table Name 改成 knn
就有連上了。

------------------------------------

以下其餘筆記，跟 Proj 內的 code 倒是無關

# 快速入門關於 python sklearn 的相關函數



## data.reshape(-1,1)

reshape(-1, 1) 可以將以 A 資料轉換成 B 資料

```
A = [ [1,2,3], [4,5,6], [7,8,9] ]
B = [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

其中， -1 代表自動計算長度，1 代表一維。

如果今天是呼叫 reshape(1, -1)，則會是以下結果

```
A = [ [1,2,3], [4,5,6], [7,8,9] ]
B = [ [1], [2], [3], [4], ..., [9]]
```



Ref : [Numpy中reshape函数、reshape(1,-1)的含义(浅显易懂，源码实例)](https://blog.csdn.net/W_weiying/article/details/82112337)



## train_test_split()

```python
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, train_size=0.7, random_state=35, stratify=y)

```

一份資料，30% 的當作 test set，70% 當作 train set。

random_state 的意義在於，你在取 random 時不是會有一個 seed 嗎 ? 
這個 seed 如果你固定他，下去跑 random，依序吐出來的那些數字之順序都會相同。

故如果有人想要重現你所使用的 test set 和 train set，random_state 只要跟你設定一樣就可以了。

``stratify=y`` : 依據 y 中的各類比例，分給 train set 和 test set，使這兩個 data set 的分類比例一樣。

假設 y 中記錄著台北市、台中市、高雄市的房子，如果極端的情況搞不好 train set 充滿了台北市的房子
這樣會導致 train 出來的 model 沒有辦法辨別其他城市的房子，目的大概是這樣。

所以基本上會按照 y 來分配，因為 y 通常是 target 而 x 通常是 feature。
(target 就是我們想要預測的結果，例如我想創一個 model 通過某些 feature 就能判斷出是哪個城市的房子。)



## load_iris()

iris 就是鳶尾花，這個 data set 是在 sklearn 內建的 example dataset，方便寫 example 使用。

簡介一下的話，
Feature 有四個，分別是花萼長度/寬度、 花瓣長度/寬度。
Target 有三種， Setosa，Versicolor 和 Virginica 三個品種。
總共資料共 150 筆，強制 print 出來也還行。

通過呼叫 ``iris.keys()`` 可以得到以下結果

```python
dict_keys(['data', 'target', 'target_names', 'DESCR', 'feature_names'])
```

故使用上

```python
from sklearn import datasets
iris = datasets.load_iris()
iris_data = iris['data']
iris_target = iris['target']
```

算好理解吧 ? 

Ref : [如何獲取資料？ Sklearn內建資料集](https://medium.com/jameslearningnote/%E8%B3%87%E6%96%99%E5%88%86%E6%9E%90-%E6%A9%9F%E5%99%A8%E5%AD%B8%E7%BF%92-%E7%AC%AC2-1%E8%AC%9B-%E5%A6%82%E4%BD%95%E7%8D%B2%E5%8F%96%E8%B3%87%E6%96%99-sklearn%E5%85%A7%E5%BB%BA%E8%B3%87%E6%96%99%E9%9B%86-baa8f027ed7b)







https://stackoverflow.com/questions/31404238/a-list-as-a-key-for-pysparks-reducebykey
