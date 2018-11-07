Table of Contents
=================

   * [事件提醒](#事件提醒)
      * [表结构](#表结构)
      * [参数介绍](#参数介绍)
      * [API接口](#api接口)
         * [Python示例](#python示例)
      * [安装使用(手动安装)](#安装使用手动安装)
      * [安装使用(Docker-compose)](#安装使用docker-compose)



# 事件提醒
- 使用人员请先修改settins里面配置信息
- 第一次使用，请打开app.py里面的`init_db`函数用于自动创建表
- 检测颗粒度默认为每小时，也可在`event_task.py`脚本自行修改

## 表结构
```mysql
+------------+--------------+------+-----+-------------------+-----------------------------+
| Field      | Type         | Null | Key | Default           | Extra                       |
+------------+--------------+------+-----+-------------------+-----------------------------+
| id         | int(11)      | NO   | PRI | NULL              | auto_increment              |
| name       | varchar(100) | YES  |     | NULL              |                             |
| content    | varchar(100) | YES  |     | NULL              |                             |
| email      | varchar(100) | YES  |     | NULL              |                             |
| advance_at | int(11)      | YES  |     | NULL              |                             |
| expire_at  | datetime     | YES  |     | NULL              |                             |
| create_at  | datetime     | NO   |     | NULL              |                             |
| update_at  | timestamp    | NO   |     | CURRENT_TIMESTAMP | on update CURRENT_TIMESTAMP |
+------------+--------------+------+-----+-------------------+-----------------------------+
```
## 参数介绍
- ID: 自增长
- name: 事件名称
- content: 事件内容描述
- Email： 需要通知人员的Email地址
- advance: 提前多少天进行提醒
- expire_at: 事件过期/到期时间
- create_at: 记录事件创建时间
- update_at: 记录事件更新时间

## API接口
- URL: http://172.16.0.101:8888/event
- 工具： Postman
- 支持： POST/PUT/DELETE

### Python示例
```python
# Body内容,根据name判断
{
    "name": "Ec2",   #名字
    "content": "服务器到期提醒",  #内容备注
    "email": "yanghongfei@qq.com, group@qq.com", #Email通知
    "advance_at": "100",  #提前多少天
    "expire_at": "2018-11-30"  #到期时间
}
```


## 安装使用(手动安装)
- 请修改对应settings里面的内容
- 创建数据库
```mysql
create database EventReminder character set utf8;
#数据表由ORM自动生成
```
- Python3环境
```bash
$ yum install xz wget -y
$ wget https://www.python.org/ftp/python/3.6.3/Python-3.6.3.tar.xz
$ xz -d  Python-3.6.3.tar.xz
$ tar xvf Python-3.6.3.tar
$ cd Python-3.6.3/
$ ./configure
$ make && make install

# 查看安装
$ python3 -V
```

- 安装依赖
```bash
$ pip3 install -r requirements.txt
```
- 守护进程
```bash
$ cp supervisord.conf /etc/supervisord.conf
$ /usr/bin/supervisord  #后台运行使用/usr/bin/supervisord &

```


## 安装使用(Docker-compose)
- 请修改对应settings里面的内容
- 首先要具有docker环境，docker推荐使用`docker-ce`
- 进入到项目目录，制作镜像启动
```bash
docker build -t event_reminder .
docker-compose up -d
```
