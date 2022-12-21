# <center>安徽科技学院自动疫情填报 V2.4 Beta(完全自动)</center>
# 简介


安徽科技学院自动完成学生健康情况填报、每日健康监测。

此源码为V2版本，V1版本也是我写的，因为专业性比较强，上手麻烦，所以写了这个V2的版本。

V2的版本只需要之前手动填报过信息，就会获取之前的信息进行自动提交。

开源不易，如果本项目对你有帮助，那么就请给个star吧。😄

同时，欢迎各位老板在线打赏。下面是我的要饭码！
[在线打赏](https://raw.githubusercontent.com/jiongjiongJOJO/AHSTU_SPCP_2/master/img/0.jpg)

# 目录

- [简介](#简介)
- [目录](#目录)
- [更新日志](#更新日志)
- [功能](#功能)
- [使用方式](#使用方式)
  - [Github Actions（不推荐）](#github-actions不推荐)
    - [1.fork本项目](#1fork本项目)
    - [2.准备需要的参数](#2准备需要的参数)
    - [3.将参数填到Secrets](#3将参数填到secrets)
    - [4.开启Actions](#4开启actions)
    - [5.进行一次push操作](#5进行一次push操作)
  - [腾讯云函数（推荐）](#腾讯云函数推荐)
    - [1.新建一个函数](#1新建一个函数)
    - [2.执行部署脚本](#2执行部署脚本)
    - [3.修改相关参数](#3修改相关参数)
    - [4.设置自动运行](#4设置自动运行)
- [通知推送方式](#通知推送方式)
- [申明](#申明)
- [参考项目](#参考项目)

# 更新日志
**V1.0** - 2021年02月18日（可能是更早，忘记了）
```
创建AHSTU_SPCP项目并开源
```
原项目地址：[AHSTU_SPCP](https://github.com/jiongjiongJOJO/AHSTU_SPCP)

**V2.0** - 2021年06月02日
```
移除了原先笨重的抓包方式
才用账号密码登录自动获取个人信息的方式提交
```

**V2.1** - 2021年09月05日
```
增加异常处理，填报错误能更好的推送！
```

**V2.2** - 2022年02月06日
```
增加疫情填报的返校信息填写（系统不知不觉更新的一个采集内容）
```

**V2.3** - 2022年02月10日
```
更改代码结构，方便腾讯云Serverless快速部署。
新增腾讯云Serverless部署脚本
```

**V2.4 Beta** - 2022年03月17日
```
【此版本为测试版本，请谨慎使用，如有疑问请向作者提出】
重构提交逻辑（完全根据上次提交的记录填报）
修改推送平台：http://www.pushplus.plus
优化部分代码警告（还有很多，等我闲了再规范化代码）
增加pushplus获取token教程
更改部分教程内容
```

# 功能

* [x] 自动填报三次随机体温（36.0~36.9）
* [x] 自动填报学生健康情况
* [x] 每日推送成功与否的信息

# 使用方式

## Github Actions（不推荐）

### 1.fork本项目

项目地址：[jiongjiongJOJO/AHSTU_SPCP_2](https://github.com/jiongjiongJOJO/AHSTU_SPCP_2)
点击右上角Fork按钮，将项目fork到自己的仓库。

### 2.准备需要的参数

学号、密码、PushPlus的token(选填)。
其中，后面提到的user为你的学号，password为你疫情填报系统的密码，send_key为PushPlus的token（不启用推送的话，可以不修改）
user和password这里是自己的信息，直接填写就行了，token的获取方式如下：
首先打开[PushPlus官网:https://www.pushplus.plus/](https://www.pushplus.plus/),然后点击登录，使用自己的微信扫码关注公众号就可以登陆成功
![](img/11.png)
接着点击【一对一推送】，点击一键复制即可
![](img/12.png)

### 3.将参数填到Secrets

首先打开Secrets页面，如下图操作
![](img/1.jpg)

Name填写为“USERINFO"即可

Value填入下面框中的内容（注意修改user，password，send_key）
```
{
    "user": "123456789",
    "password": "123456789",
    "send_key": "123456789"
}
```

![](img/2.jpg)



### 4.开启Actions

默认`Actions`处于禁止状态，在`Actions`选项中开启`Actions`功能，把那个绿色的长按钮点一下。如果看到左侧工作流上有黄色`!`号，还需继续开启。

![](img/3.jpg)

### 5.进行一次push操作

`push`操作会触发工作流运行。

删除掉`README.md`即可。完成后，每天将自动完成每日任务。

## 腾讯云函数（推荐）

### 1.新建一个函数
打开[腾讯云函数](https://console.cloud.tencent.com/scf/list)，登录账号（可以用QQ登录），然后点击“新建”
![](img/4.jpg)
然后根据下图步骤填写信息
![](img/5.jpg)
接着点击编辑按钮关掉日志功能（很重要，因为日志会产生费用，不及时充值会停止运行）
![](img/6.jpg)
修改超时时间和关闭日志功能，修改完点保存就行了
![](img/7.jpg)

### 2.执行部署脚本
```shell
curl -O https://gitee.com/jiongjiongJOJO/AHSTU_SPCP_2/raw/main/tencentServerless.sh && bash ./tencentServerless.sh
```

### 3.修改相关参数
打开函数代码，找到index.py文件，修改图中圈出的内容（不要删除或添加多余的空格等内容）
![](img/8.jpg)
其中，user后面填写自己的学号，password后面填写密码，send_key后面填写[PushPlus的token](#pushplus机器人)（可以在下方获取）
修改完成后点击下方的部署，等待十秒左右，会提示部署完成。

### 4.设置自动运行
选择创建触发器
![](img/9.jpg)
设置触发周期
其中Cron表达式中包含空格，下方内容为图中的表达式，可以直接复制使用
```
0 30 8 * * * *
```
![](img/10.jpg)
点击提交后，就配置完成了，每天8:30分自动执行脚本。

# 通知推送方式

## pushplus机器人
只需要一个`token`，参考[获取pushplus的token](https://www.pushplus.plus/)。

# 申明

本项目仅用于学习,不建议使用该脚本进行自动化操作，否则作者概不负责。
如果你的体温、位置等信息发生了变化，请及时向学校报备，严禁任何人逃避异常问题。

# 参考项目

[srcrs/UnicomTask](https://github.com/srcrs/UnicomTask)，参考了该项目的README.md文档
