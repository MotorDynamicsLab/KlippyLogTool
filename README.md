



# 安装环境



**python版本：3.9.0**



**安装依赖 ：执行 pip install -r requirements.txt 来安装所依赖的组件包**





# 基本操作

## 设置区间

可以设置分析的x轴的间隔区间，**不同的区间分析结果会不一样，如果设置区间过大，可能看不到一些波形细节**

![image-20240822102753275](http://tyk-bucket.oss-cn-shenzhen.aliyuncs.com/img/image-20240822102753275.png)



## 选择隐藏/显示线



点击途中框内的目标，可选择隐藏/显示目标线段

![image-20240822103111875](http://tyk-bucket.oss-cn-shenzhen.aliyuncs.com/img/image-20240822103111875.png)



# 相关问题





## x轴的含义

x轴是stats文件中的行间隔



![image-20240822101753771](http://tyk-bucket.oss-cn-shenzhen.aliyuncs.com/img/image-20240822101753771.png)





它的值*采样间隔 为stats文件所对应的行数。如下图 50`*`100=5000，即50就是stat文件中的第5000行

![image-20240822101903365](http://tyk-bucket.oss-cn-shenzhen.aliyuncs.com/img/image-20240822101903365.png)







## 判断断连时刻

类似下图这种尖尖基本就是断连

![image-20240822102636758](http://tyk-bucket.oss-cn-shenzhen.aliyuncs.com/img/image-20240822102636758.png)





## 分析错误对于图中的那个位置



点击丢包分析，复制一个错误信息

![Snipaste_2024-08-21_16-17-58](http://tyk-bucket.oss-cn-shenzhen.aliyuncs.com/img/Snipaste_2024-08-21_16-17-58.png)![](http://tyk-bucket.oss-cn-shenzhen.aliyuncs.com/img/typora-icon2.png)


打开当前log和stats文件

![image-20240821162113180](http://tyk-bucket.oss-cn-shenzhen.aliyuncs.com/img/image-20240821162113180.png)





在log中搜索错误信息，找到错误前的依据stats，并复制

![image-20240821162215653](http://tyk-bucket.oss-cn-shenzhen.aliyuncs.com/img/image-20240821162215653.png)





从stats文件中搜索，找到对应的行数，如下

![image-20240821162255476](http://tyk-bucket.oss-cn-shenzhen.aliyuncs.com/img/image-20240821162255476.png)



从而得知566行的位置大概在下图位置附件

![image-20240821162345698](http://tyk-bucket.oss-cn-shenzhen.aliyuncs.com/img/image-20240821162345698.png)