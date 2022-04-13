# Food Robber脚本使用指南

**请不要传播此脚本**

您只需要修改robFood的初始参数即可。

首先打开您需要抢购的网站：

[理发](https://dailyreport.sjtu.edu.cn/haircut/#/)

[超市购物](https://dailyreport.sjtu.edu.cn/market/#/)

查询你的`JSESSIONID`和`dailyreport.sjtu`参数内容。

注意：这两个网站的`JSESSIONID`是不同的，注意区分；在运行脚本前您需要刷新页面以获取**最新**的`JSESSIONID`，否则可能导致失败。另外，只能提前几秒钟开始运行脚本，否则，**网站将检测到你的行为**把你给屏蔽掉。

## 理发

示例：

`robFood('JSESSIONID','dailyreport.sjtu','haircut','bus','TWO','2022-04-14','16:00')`

1. `JSESSIONID`
2. `dailyreport.sjtu`
3. 与选择项目有关的一个参数，理发的话就是`haircut`
4. 与选择项目有关的一个参数，理发的话就是`bus`
5. 地点选择，这里有`TWO`,`THIRD`,`FOURTH`
6. 日期，必须按这种格式填写。应该填写明天的日期
7. 时间，如果没有抢到，脚本会再尝试抢其他时间点，必须是**整点**

## 教超/罗森

`robFood('JSESSIONID','dailyreport.sjtu','market','market','YLYLS','2022-04-14','14:00')`

1. `JSESSIONID`
2. `dailyreport.sjtu`
3. 与选择项目有关的一个参数，这里的话就是`market`
4. 与选择项目有关的一个参数，这里的话就是`market`
5. 地点选择，这里有`XQJYCS`（教超）,`YLYLS`（罗森）
6. 日期，必须按这种格式填写。应该填写明天的日期
7. 时间，如果没有抢到，脚本会再尝试抢其他时间点，必须是**整点**

## 其他说明

可选参数：`thread_num`，可指定线程数量，默认是10.