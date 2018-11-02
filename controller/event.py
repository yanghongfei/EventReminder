#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/24 17:58
# @Author  : Fred Yang
# @File    : event.py
# @Role    : 事件提醒Handler


import json
import tornado.web
from database import db_session
from models import EventReminder


class EventHandler(tornado.web.RequestHandler):
    """事件路由 增删改查"""

    def get(self, *args, **kwargs):
        return self.write(dict(status=0, msg='Hello,EventHander!'))

    def post(self, *args, **kwargs):
        '''新增一条事件'''
        data = json.loads(self.request.body.decode("utf-8"))

        name = data.get('name', None)
        content = data.get('content', None)
        email = data.get('email', None)
        advance_at = data.get('advance_at', None)
        expire_at = data.get('expire_at', None)

        try:
            name_info = db_session.query(EventReminder).filter(EventReminder.name == name).first()
            if name_info:
                return self.write(dict(status=-1, msg="name already exist..."))
            else:
                print('1111')
                db_session.add(
                    EventReminder(name=name, content=content, email=email, advance_at=advance_at, expire_at=expire_at))
                db_session.commit()
                resp = {
                    'status': 0,
                    'msg': '添加成功'
                }
                return self.write(resp)
        except Exception as e:
            print(e)
            db_session.rollback()

    def put(self, *args, **kwargs):
        '''更新信息'''
        data = json.loads(self.request.body.decode("utf-8"))
        name = data.get('name', None)
        content = data.get('content', None)
        email = data.get('email', None)
        advance_at = data.get('advance_at', None)
        expire_at = data.get('expire_at', None)

        try:
            event_info = {
                "content": content,
                "email": email,
                "advance_at": advance_at,
                "expire_at": expire_at,
            }
            db_session.query(EventReminder).filter(EventReminder.name == name).update(event_info)
            db_session.commit()
            resp = {
                'status': 0,
                'msg': '更新成功'
            }
            return self.write(resp)
        except Exception as e:
            print(e)
            db_session.rollback()

    def delete(self, *args, **kwargs):
        data = json.loads(self.request.body.decode("utf-8"))
        name = data.get('name', None)
        try:
            db_session.query(EventReminder).filter(EventReminder.name == name).delete(synchronize_session=False)
            db_session.commit()
            resp = {
                'status': 0,
                'msg': '删除成功'
            }
            return self.write(resp)
        except Exception as e:
            print(e)
            db_session.rollback()
