



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

1. (傳入參數, 回傳的分數) 以此 pair 記錄至 DB 中，並且可以透過前端查詢
2. 提供更多對於 KNN 參數之調整
   - 不同計算距離方式，加入至前端提供選擇
   - 可以上傳自己的 txt file



已知可能 bug :

1. 已有在 spark container 內串過了，需要把 ``import final`` 取消註解
   和更改 ``test.KNN() -> final.KNN()``
   不過 ``buildin_iris`` 的選項還沒跑過
2. container 必須要有對應 port : ``-p 5678:5000``，
   且 container 內的 flask app 必須帶有參數 ``host='0.0.0.0'`` 才能正常在 host 吃到
   (這個參數已經在 code 中了)
3. 網頁端執行參數不可為空。



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
