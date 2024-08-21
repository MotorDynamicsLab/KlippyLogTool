



# 安装环境



**python版本：3.9.0**



**requirements.txt文件 ：执行 pip install -r requirements.txt 来安装所依赖的组件包**









# 使用说明



## x轴说明

x轴是stats文件中的行间隔，它的值*采样间隔 为stats文件对应的行数。可根据这个来看图对应的位置，在log的哪个位置，反之亦然



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
